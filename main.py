import os
import streamlit as st
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from streamlit_chat import message
from config import Config
from bot_manager import BotManager

# Initialize BotManager
bot_manager = BotManager(Config.OPENAI_API_KEY)
# Set up Streamlit page
st.set_page_config(page_title="Unified Bot Management", layout="wide")
# Inject custom CSS to make the title sticky
st.markdown("""
    <style>
        .sticky-title {
            position: sticky;
            top: 0;
            background-color: white;
            z-index: 999;
            padding-top: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar UI for Unified Bot Management
with st.sidebar:
    st.title("Unified Bot Management")
    # Button to toggle the bot creation form
    if st.button("Create New Bot"):
        st.session_state['show_create_bot_form'] = True

    # Display bot creation form only when 'show_create_bot_form' is True
    if st.session_state.get('show_create_bot_form', False):
        with st.form(key='new_bot_form'):
            name = st.text_input("Bot Name")
            model = st.selectbox("Model", ["gpt-3.5", "Other Models..."])
            context_prompt = st.text_area("Context Prompt")
            temperature = st.slider("Temperature", 0.0, 1.0, 0.5)
            documents = st.file_uploader("Upload Documents", accept_multiple_files=False)
            print(documents)
            if documents is not None:
                DATA_DIR = name
                # Create the data directory if it doesn't exist
                if not os.path.exists(DATA_DIR):
                    os.makedirs(DATA_DIR)
            create_button = st.form_submit_button("Create Bot")

        if create_button:
            if not name or not model or not context_prompt or temperature is None:
                st.warning("Please fill in all required fields.")
            else:
                # Process and add the bot
                if documents is not None:
                    DATA_DIR = os.path.join('data', name)  # Directory path
                    if not os.path.exists(DATA_DIR):
                        os.makedirs(DATA_DIR)
                    
                    # Save the uploaded file to the directory
                    file_path = os.path.join(DATA_DIR, documents.name)
                    with open(file_path, "wb") as f:
                        f.write(documents.getbuffer())

                input_dir = DATA_DIR if documents is not None else None
                bot_manager.add_bot(name, model, context_prompt, temperature, input_dir)
                st.session_state['show_create_bot_form'] = False

    # Bot selection and deletion
    if 'selected_bot_name' not in st.session_state:
        st.session_state['selected_bot_name'] = list(bot_manager.get_all_bots())[0]

    selected_bot_name = st.selectbox("Select a bot to chat with:", list(bot_manager.get_all_bots()), index=0)

    if selected_bot_name in bot_manager.user_bots:
        if st.button("Delete Selected Bot"):
            bot_manager.delete_bot(selected_bot_name)
            st.experimental_rerun()
    if st.button("Clear Chat"):
        selected_bot = bot_manager.get_bot(selected_bot_name)
        if selected_bot:
            selected_bot.clear_conversation()
            # Also clear the stored conversation in Streamlit's session state
            st.session_state[f'responses_{selected_bot_name}'] = []
            st.session_state[f'requests_{selected_bot_name}'] = []
            st.success(f"Conversation with {selected_bot_name} has been cleared.")

# Main chat area
title_container = st.container()
chat_container = st.container()
with title_container:
    # Sticky title
    st.markdown(f'<div class="sticky-title"><h1>Chat with {selected_bot_name}</h1></div>', unsafe_allow_html=True)
with chat_container:
    # Chat content
    response_container = st.container()
    text_container = st.container()
    with text_container:
        query = st.text_input("Type your message here: ", key=f"input_{selected_bot_name}")
        if query:
            selected_bot = bot_manager.get_bot(selected_bot_name)
            if selected_bot:
                # Check if documents are provided and use the appropriate method
                if selected_bot.documents:
                    response = selected_bot.query_document(query)
                else:
                    response = selected_bot.chat(query)
                if f'responses_{selected_bot_name}' not in st.session_state:
                    st.session_state[f'responses_{selected_bot_name}'] = ["How can I assist you?"]
                if f'requests_{selected_bot_name}' not in st.session_state:
                    st.session_state[f'requests_{selected_bot_name}'] = []
                st.session_state[f'requests_{selected_bot_name}'].append(query)
                st.session_state[f'responses_{selected_bot_name}'].append(response)
            else:
                st.error("Selected bot not found.")
        else:
            response = None

    with response_container:
        if f'responses_{selected_bot_name}' in st.session_state:
            for i in range(len(st.session_state[f'responses_{selected_bot_name}'])):
                message(st.session_state[f'responses_{selected_bot_name}'][i], key=f"{selected_bot_name}_{i}")
                if i < len(st.session_state[f'requests_{selected_bot_name}']):
                    message(st.session_state[f"requests_{selected_bot_name}"][i], is_user=True, key=f"{selected_bot_name}_{i}_user")
