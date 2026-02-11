from uuid import uuid4
from pymongo import MongoClient
from datetime import datetime, timedelta
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin

# pymongo==4.8

class MongoSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, store=None):
        CallbackDict.__init__(self, initial)
        self.sid = sid
        self.modified = False
        self.store = store

    def clear(self):
        self.store.delete_one({'sid': self.sid})
        super(MongoSession, self).clear()

    def count(self, username=None):
        filter = {'data.user': {'$exists': True}}
        if username is not None:
            filter['data.user.username'] = username
        return self.store.find(filter).count()


class MongoSessionInterface(SessionInterface):
    def __init__(self, config={}, app=None):
        if config == {}:
            raise Exception('MongoSessionInterface misconfiguration')
        expireAfterSeconds = 3600
        mongo_uri = f"mongodb://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?authSource=admin"
        client = MongoClient(mongo_uri)
        self.store = client[config['database']][config['collection']]
        if app is not None:
            expireAfterSeconds = app.permanent_session_lifetime.total_seconds()
        try:
            self.store.ensure_index('sid')
            self.store.ensure_index('modified', expireAfterSeconds=expireAfterSeconds)
        except:
            self.store.drop_indexes()

    def open_session(self, app, request):
        print('requrest: %s', request)
        sid = request.cookies.get(app.session_cookie_name)
        if sid:
            stored_session = self.store.find_one({'sid': sid})
            if stored_session:
                if stored_session.get('expiration') > datetime.utcnow():
                    return MongoSession(initial=stored_session['data'],
                                        sid=stored_session['sid'], store=self.store)
        sid = str(uuid4())
        return MongoSession(sid=sid, store=self.store)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            response.delete_cookie(app.session_cookie_name, domain=domain)
            return
        if self.get_expiration_time(app, session):
            expiration = self.get_expiration_time(app, session)
        else:
            expiration = datetime.utcnow() + timedelta(seconds=app.permanent_session_lifetime.total_seconds())
        self.store.update_one(
            {'sid': session.sid},
            {'$set': {
                'sid': session.sid,
                'data': dict(session),  # Convert session to a dictionary
                'modified': datetime.utcnow(),
                'expiration': expiration
            }},
            upsert=True
        )
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=self.get_expiration_time(app, session),
                            httponly=True, domain=domain)