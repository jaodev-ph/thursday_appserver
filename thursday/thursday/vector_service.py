import chromadb
from chromadb.utils import embedding_functions
from logging import getLogger

from thursday.settings import VECTOR_CONFIG

log = getLogger('thursday.vectors')
import ollama

vector_client = chromadb.HttpClient(host=VECTOR_CONFIG.get('host'), port=VECTOR_CONFIG.get('port'))
log.info('vectorDB connecting: %s', vector_client)

class VectorService:
    def __init__(self, collection_name="default_collection"):
        """Initialize service with a specific collection."""
        self.collection_name = collection_name
        self.collection = vector_client.get_or_create_collection(collection_name)


    def add(self, ids=None, documents=None, metadatas=None):
        ids = ids
        documents = documents
        metadatas = metadatas
        embeddings = []
        if documents:
            response = ollama.embed(
                model="mxbai-embed-large",
                input=documents
            )
            log.info('response: %s', response)
            embeddings = response.embeddings
        return self.collection.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)

    def batch_add(self, docs=None):
        docs = docs or []
        ids = [d["id"] for d in docs]
        documents = [d["doc"] for d in docs]
        metadatas = [d.get("meta", {}) for d in docs]
        return self.add(ids=ids, documents=documents, metadatas=metadatas)