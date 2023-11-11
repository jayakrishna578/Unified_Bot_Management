import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        self.conn.commit()

    def insert_data(self, table_name, columns, data):
        self.cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({data})")
        self.conn.commit()

    def query_data(self, table_name, columns):
        self.cursor.execute(f"SELECT {columns} FROM {table_name}")
        return self.cursor.fetchall()
