# -*- coding: utf-8 -*-
# ~
# Swift API Dispatcher
# entropysoln
# ~

from werkzeug.middleware.dispatcher import DispatcherMiddleware

# API Versions
from api.v1 import app as v1
# app.config['APPLICATION_ROOT'] = '/api'

applications = {
    '/v1': v1
}
app = DispatcherMiddleware(v1, applications)
