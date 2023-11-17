import os
from dotenv import load_dotenv
import streamlit as st

# Load .env file
load_dotenv()

class Config:
    #OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    st.secrets['OPENAI_API_KEY']

    @staticmethod
    def validate():
        missing = []
        if not Config.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")

# Validate configuration at import
Config.validate()