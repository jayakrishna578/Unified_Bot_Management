import os
import streamlit as st
from dotenv import load_dotenv
from covid_protocol_bot import CovidProtocolBot
from bot import Bot
from stock_retrieval import StockDataRetrievalBot
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from streamlit_chat import message
from utils import *

# Function definitions
def initialize_bots():
    dotenv_path = '.env'
    load_dotenv(dotenv_path)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    covid_bot = CovidProtocolBot()
    general_bot = Bot("GeneralBot", "gpt-3.5", "You are a helpful assistant.", 0.5, [], openai.api_key)
    stock_bot = StockDataRetrievalBot(api_key=openai.api_key)
    return {
        "CovidProtocolBot": covid_bot,
        "GeneralBot": general_bot,
        "StockDataRetrievalBot": stock_bot
    }


# App setup
st.set_page_config(page_title="Unified Bot Management", layout="wide")
bots = initialize_bots()

# Sidebar
st.sidebar.title("Unified Bot Management")
previous_bot_name = st.session_state.get('previous_bot_name', None)
selected_bot_name = st.sidebar.radio("Select a bot:", list(bots.keys()))
st.session_state['selected_bot_name'] = selected_bot_name

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)

if selected_bot_name != previous_bot_name:
    st.session_state['previous_bot_name'] = selected_bot_name

# Main chat area
chat_container = st.container()
with chat_container:
    st.title(f"Chat with {selected_bot_name}")
    response_container = st.container()
    textcontainer = st.container()
    with textcontainer:
        query = st.text_input("Type your message here: ", key="input")
        if query:
            response = bots[selected_bot_name].chat(query)
            st.session_state.requests.append(query)
            st.session_state.responses.append(response)
        else:
            response = None
            refined_query = ""

    with response_container:
        if st.session_state['responses']:
            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

