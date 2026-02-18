import chromadb
from logging import getLogger

from thursday.settings import VECTOR_CONFIG

log = getLogger('thursday.vectors')

vector_client = chromadb.HttpClient(host=VECTOR_CONFIG.get('host'), port=VECTOR_CONFIG.get('port'))

log.info('vector_client connecting: %s', vector_client)


class VectorService:
    def __init__(self, collection_name="default_collection"):
        """Initialize service with a specific collection."""
        self.collection_name = collection_name
        self.collection = vector_client.get_or_create_collection(collection_name)

    # ------------------------------
    # CRUD Methods
    # ------------------------------

    def add(self, ids=None, documents=None, metadatas=None):
        ids = ids or []
        documents = documents or []
        metadatas = metadatas or []
        return self.collection.add(ids=ids, documents=documents, metadatas=metadatas)

    def batch_add(self, docs=None):
        docs = docs or []
        ids = [d["id"] for d in docs]
        documents = [d["doc"] for d in docs]
        metadatas = [d.get("meta", {}) for d in docs]
        return self.add(ids=ids, documents=documents, metadatas=metadatas)

    def search(self, query="hello", n_results=1):
        return self.collection.query(query_texts=[query], n_results=n_results)

    def search_with_metadata(self, query="hello", filter_metadata=None, n_results=1):
        return self.collection.query(query_texts=[query], n_results=n_results, where=filter_metadata or {})

    def get_all(self):
        return self.collection.get()

    def delete(self, ids=None):
        ids = ids or []
        return self.collection.delete(ids=ids)

    def drop_collection(self):
        return self.collection.delete()

    def count(self):
        return self.collection.count()