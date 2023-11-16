import os
from bot import Bot
from covid_protocol_bot import CovidProtocolBot
from stock_retrieval import StockDataRetrievalBot
from langchain.memory import ConversationBufferMemory
import json

class BotManager:
    def __init__(self, openai_api_key):
        self.default_bots = {}
        self.user_bots = {}
        self.openai_api_key = openai_api_key
        self.user_bots_file = "user_bots.json"
        self.initialize_default_bots()
        self.load_user_bots()

    def initialize_default_bots(self):
        # Initialize default bots here
        self.default_bots["GeneralBot"] = Bot("GeneralBot", "gpt-3.5", "You are a helpful assistant.", 0.5, None, self.openai_api_key)
        self.default_bots["CovidProtocolBot"] = CovidProtocolBot()
        #self.default_bots["StockDataRetrievalBot"] = StockDataRetrievalBot(api_key=self.openai_api_key)

    def add_bot(self, name, model, context_prompt, temperature, documents):
        # Create and add a new bot to user_bots
        new_bot = Bot(name, model, context_prompt, temperature, documents, self.openai_api_key)
        self.user_bots[name] = new_bot

        # Save bot configuration
        bot_config = {
            "name": name,
            "model": model,
            "context_prompt": context_prompt,
            "temperature": temperature,
            "documents": documents
        }
        self._save_bot_config(bot_config)

    def get_bot(self, name):
        # Retrieve a bot by name
        return self.user_bots.get(name) or self.default_bots.get(name)

    def get_all_bots(self):
        # Get all available bots
        return {**self.default_bots, **self.user_bots}.keys()

    def delete_bot(self, name):
        # Delete a user-added bot
        if name in self.user_bots:
            del self.user_bots[name]
            self.save_user_bots()

    def _save_bot_config(self, bot_config):
        # Load existing configs
        if os.path.exists(self.user_bots_file):
            with open(self.user_bots_file, "r") as file:
                configs = json.load(file)
        else:
            configs = []

        # Add new config and save
        configs.append(bot_config)
        with open(self.user_bots_file, "w") as file:
            json.dump(configs, file)

    def load_user_bots(self):
        # Load user bots from a file
        if os.path.exists(self.user_bots_file) and os.path.getsize(self.user_bots_file) > 0:
            with open(self.user_bots_file, "r") as file:
                configs = json.load(file)
                for config in configs:
                    self.user_bots[config['name']] = Bot(
                        config['name'],
                        config['model'],
                        config['context_prompt'],
                        config['temperature'],
                        config['documents'],
                        self.openai_api_key
                    )
        else:
            # The file doesn't exist or is empty, so initialize an empty dict
            self.user_bots = {}

    def save_user_bots(self):
        # Update the user_bots.json file
        with open(self.user_bots_file, 'w') as file:
            configs = []
            for name, bot in self.user_bots.items():
                bot_config = {
                    "name": name,
                    "model": bot.model,
                    "context_prompt": bot.context_prompt,
                    "temperature": bot.temperature,
                    "documents": bot.documents  # Make sure this aligns with your Bot class
                }
                configs.append(bot_config)
            json.dump(configs, file)
