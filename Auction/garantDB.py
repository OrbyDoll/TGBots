import sqlite3


class GarantDB:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_table(self):
        with self.connection:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS users(
                    user_id TEXT,
                    offers TEXT,
                    balance TEXT,
                    ban TEXT,
                    nick TEXT);
                """
            )

    def get_balance(self, user_id):
        with self.connection:
            res = self.cursor.execute(
                "SELECT `balance` FROM `users` WHERE `user_id` = ?", (user_id,)
            ).fetchone()
            return res

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)
            ).fetchall()
            return bool(result)

    def check_ban(self, user_id):
        with self.connection:
            res = self.cursor.execute(
                "SELECT `ban` from `users` WHERE `user_id` = ?", (user_id,)
            ).fetchone()
            return res[0]
