import os
import openai
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
import logging

from llama_index import (GPTVectorStoreIndex, ServiceContext, SimpleDirectoryReader)
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

class Bot:
    def __init__(self, name, model, context_prompt, temperature, documents_dir, openai_api_key):
        self.name = name
        self.model = model
        self.context_prompt = context_prompt
        self.temperature = temperature
        self.openai_api_key = openai_api_key
        self.logger = logging.getLogger(self.name)
        self._setup_logging()

        if documents_dir is None or not os.path.exists(documents_dir) or not os.path.isdir(documents_dir):
            # Handle the case where the directory is None or does not exist
            self.documents = None
        else:
            self.documents = documents_dir

        if self.documents is not None:
            data = SimpleDirectoryReader(self.documents).load_data()
            self.client = QdrantClient(":memory:")
            self.service_context = ServiceContext.from_defaults(chunk_size=512)
            self.vector_store = QdrantVectorStore(client=self.client, collection_name="Covid19_latest_guidelines")
            self.index = GPTVectorStoreIndex.from_documents(data, vector_store=self.vector_store, service_context=self.service_context, show_progress=True)
            self.query_engine = self.index.as_query_engine(similarity_top_k=2)
        else:
            # Initialize the langchain components
            self.llm = OpenAI(openai_api_key=self.openai_api_key)
            self.memory = ConversationBufferMemory(memory_key="chat_history", k=5)
            self.prompt = PromptTemplate(
                input_variables=['chat_history', 'question'],
                template=f"{self.context_prompt}\nchat history: {{chat_history}}\nHuman: {{question}}\nAI:"
            )
            self.llmchain = LLMChain(llm=self.llm, memory=self.memory, prompt=self.prompt)

    def _setup_logging(self):
        if not self.logger.handlers:
            # Configure logger
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def chat(self, query):
        try:
            if query:
                #conversation_string = self._get_conversation_string()
                response = self.llmchain.predict(question=query)
                return response
        except Exception as e:
            self.logger.error(f"Error during chat: {e}")
            return "Sorry, I encountered an error."
        
    def query_document(self,query):
        try:
            if query:
                response = self.query_engine.query(query)
                return response.response
        except Exception as e:
            self.logger.error(f"Error during chat: {e}")
            return "Sorry, I encountered an error."

    def _get_conversation_string(self):
        conversation_string = ""
        for i in range(len(st.session_state['responses'])-1):        
            conversation_string += f"Human: {st.session_state['requests'][i]}\nBot: {st.session_state['responses'][i+1]}\n"
        return conversation_string
    
    def _load_and_process_documents(self, documents_dir):
        # Check if the directory exists
        if documents_dir == None:
            return None
        else:
            if not os.path.exists(documents_dir) or not os.path.isdir(documents_dir):
                # Handle the case where the directory does not exist or is not a directory
                return []

            processed_documents = []
            for filename in os.listdir(documents_dir):
                file_path = os.path.join(documents_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    # Process each document as needed
                    # For example, read the file content
                    content = file.read()
                    # Add additional processing as required
                    processed_documents.append(content)  # Adjust this based on the expected format

            return processed_documents
        
    def clear_conversation(self):
        # Assuming the ConversationBufferMemory has a method to clear its memory
        # If not, this method needs to be implemented in the ConversationBufferMemory class
        self.memory.clear()

