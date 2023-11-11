from bot import Bot
from database import Database

class QueryBot(Bot):
    def __init__(self, name, model, context_prompt, temperature, documents_to_query, db_name):
        super().__init__(name, model, context_prompt, temperature, documents_to_query)
        self.db = Database(db_name)

    def query_stock_data(self, table_name, columns):
        return self.db.query_data(table_name, columns)
