import chromadb
from chromadb.utils import embedding_functions
from logging import getLogger

from thursday.settings import VECTOR_CONFIG

log = getLogger('thursday.vectors')
from ollama import Ollama

ollama_client = Ollama()
vector_client = chromadb.HttpClient(host=VECTOR_CONFIG.get('host'), port=VECTOR_CONFIG.get('port'))
log.info('vectorDB connecting: %s', vector_client)


def get_ollama_embeddings(texts: list[str], model: str = "mxbai-embed-large"):
    """
    Calls Ollama Python client to get embeddings for a batch of texts.
    Returns a list of lists of floats.
    """
    # Ollama Python embed API expects a list of strings
    result = ollama_client.embed(model=model, input=texts)
    return result.embeddings  # list[list[float]]

class OllamaEmbedding(embedding_functions.EmbeddingFunction):
    def __init__(self, model_name="mxbai-embed-large"):
        self.model_name = model_name

    def __call__(self, texts: list[str]):
        return get_ollama_embeddings(texts, model=self.model_name)


ollama_embed_fn = OllamaEmbedding(model_name="mxbai-embed-large")

class VectorService:
    def __init__(self, collection_name="default_collection"):
        """Initialize service with a specific collection."""
        self.collection_name = collection_name
        existing = [c.name for c in vector_client.list_collections()]
        
        if collection_name in existing:
            # don’t pass embedding_function again
            self.collection = vector_client.get_or_create_collection(collection_name)

        else:
            self.collection = vector_client.get_or_create_collection(
                collection_name,
                embedding_function=ollama_embed_fn,
            )

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