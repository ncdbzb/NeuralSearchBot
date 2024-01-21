import sqlite3
import os
from config_data.config import Config, load_config

config: Config = load_config('.env')


class Database:
    def __init__(self, db_file=os.path.join('database', config.db.db_name)):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def get_data(self, query):
        with self.connection:
            return self.cursor.execute(query).fetchall()

    def get_descriptions(self):
        with self.connection:
            items = self.cursor.execute('SELECT describtion FROM neural_networks;').fetchall()
            return list(map(lambda x: x[0], items))

    def get_all_ids(self):
        with self.connection:
            users_ids = self.cursor.execute('SELECT user_id FROM users')

            return [int(user_id[0]) for user_id in users_ids]
