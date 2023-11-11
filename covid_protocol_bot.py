# File: covid_protocol_bot.py
from llama_index import (GPTVectorStoreIndex, ServiceContext, SimpleDirectoryReader)
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

class CovidProtocolBot:
    def __init__(self):
        client = QdrantClient(":memory:")
        documents = SimpleDirectoryReader('data/').load_data()
        service_context = ServiceContext.from_defaults(chunk_size=512)
        vector_store = QdrantVectorStore(client=client, collection_name="Covid19_latest_guidelines")
        self.index = GPTVectorStoreIndex.from_documents(documents, vector_store=vector_store, service_context=service_context, show_progress=True)
        self.query_engine = self.index.as_query_engine(similarity_top_k=2)

    def chat(self, query):
        # The method name has been changed from generate_response to chat
        response = self.query_engine.query(query)
        return response.response
