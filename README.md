Title: Unified Bot Management System

Description:
This project is a Unified Bot Management System, a Streamlit-based web application for creating, managing, and interacting with chatbots. It utilizes OpenAI's GPT-3 and GPT-4 models for natural language processing and SQLite for database management.

Project Structure:
main.py: The entry point of the application. It contains the Streamlit interface and the logic to manage the chatbots.
bot.py: Defines the Bot class for creating and managing individual chatbots.
database.py: Contains the Database class for interacting with the SQLite database.
stock_data_retrieval_bot.py: Implements the StockDataRetrievalBot class for fetching stock data.
query_bot.py: Includes the QueryBot class for querying the database for stock data.

Features:
Bot Creation and Management: Create and manage various types of chatbots.
Document Upload: Upload documents for bots to use in responses.
Chat Interface: Interact with bots through a real-time chat interface.
Stock Data Retrieval: Specialized bot for fetching and presenting stock data.
Database Querying: A bot designed to query a SQLite database for specific information.

Installation:
Prerequisites
Python 3.8+
OpenAI API key

Setup:
Clone the repository: 
git clone [repository URL]

Navigate to the project directory:
cd Unified_bot_management

Install dependencies:
pip install -r requirements.txt

Running the Application:
streamlit run main.py

Usage:
Start the application and use the sidebar to create or manage bots.
Interact with the bots using the chat interface.
