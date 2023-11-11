import os
import openai
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)
api_key = os.getenv("OPENAI_API_KEY")

class Bot:
    def __init__(self, name, model, context_prompt, temperature, documents_to_query, openai_api_key):
        self.name = name
        self.model = model
        self.context_prompt = context_prompt
        self.temperature = temperature
        self.documents_to_query = documents_to_query
        self.openai_api_key = openai_api_key

        # Initialize the langchain components
        self.llm = OpenAI(openai_api_key=self.openai_api_key)
        self.memory = ConversationBufferMemory(memory_key="chat_history", k=5)
        self.prompt = PromptTemplate(
            input_variables=['chat_history', 'question'],
            template=f"""{self.context_prompt}
            chat history: {{chat_history}}
            Human: {{question}}
            AI:"""
        )
        self.llmchain = LLMChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt
        )
    
    def get_conversation_string(self):
        conversation_string = ""
        for i in range(len(st.session_state['responses'])-1):        
            conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
            conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
        return conversation_string

    def chat(self, query):
        if query:
            with st.spinner("typing..."):
                #response = self.conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
                conversation_string = self.get_conversation_string()
                #refined_query = utils.query_refiner(conversation_string, query)
                #st.subheader("Refined Query:")
                #st.write(refined_query)
                response = self.llmchain.predict(question=query)

        return response
