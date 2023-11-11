# stock_data_retrieval_bot.py

import openai
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.output_parsers import GuardrailsOutputParser
from langchain.prompts import PromptTemplate
from langchain.utilities import GoogleSerperAPIWrapper
import sqlite3
from datetime import datetime

class StockDataRetrievalBot:
    def __init__(self, api_key):
        self.llm = OpenAI(temperature=0)
        self.stock_data_retrieval = GoogleSerperAPIWrapper(api_key=api_key)

        tools = [
            Tool(
                name="Intermediate Answer",
                func=self.stock_data_retrieval.run,
                description="Fetches stock data using Google Search",
            )
        ]

        self.stock_data_agent = initialize_agent(
            tools, self.llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True
        )

    def retrieve_and_store_stock_data(self):
        # Fetch the stock data
        query = "Get me the top 10 stocks with the most significant gains and losses from the previous trading day"
        stock_data = self.stock_data_agent.run(query)

        # Define the guardrails specification for stock data
        rail_spec = """
        <rail version="0.1">
        <output>
        <object name="stock_info">
        <array name="top_gainers">
        <object>
            <string name="symbol"></string>
            <float name="gain"></float>
        </object>
        </array>
        <array name="top_losers">
        <object>
            <string name="symbol"></string>
            <float name="loss"></float>
        </object>
        </array>
        </object>
        </output>
        <prompt>
        Given the following stock market data, please extract a dictionary that contains the top gainers and losers.

        ${api_result}

        ${gr.complete_json_suffix_v2}
        </prompt>
        </rail>
        """

        # Parse the stock data using guardrails
        output_parser = GuardrailsOutputParser.from_rail_string(rail_spec, api=openai.ChatCompletion.create)
        prompt = PromptTemplate(
            template=output_parser.guard.prompt.escape(),
            input_variables=output_parser.guard.prompt.variable_names,
        )

        # Structure the output
        structured_output = self.llm(prompt.format_prompt(api_result=stock_data).to_string())

        # Connect to the database (SQLite for example)
        conn = sqlite3.connect('stock_data.db')
        c = conn.cursor()

        # Create a table to store the data (if it does not exist)
        c.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                date TEXT,
                symbol TEXT,
                gain REAL,
                loss REAL,
                category TEXT
            )ss
        ''')

        # Insert the structured data into the database
        today_date = datetime.now().strftime('%Y-%m-%d')
        # Parse the structured_output and insert each stock into the database
        # ... (Your code to parse the structured_output and insert data into the database)

        # Close the database connection
        conn.close()

        return structured_output  # Return the structured output
