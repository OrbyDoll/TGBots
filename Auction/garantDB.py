import sqlite3


def getSummFromString(str):
    spl_str = str.split()
    for i in range(len(spl_str)):
        if spl_str[i] == "сумму":
            return float(spl_str[i + 1])


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

    def ban(self, user_id):
        with self.connection:
            try:
                return self.cursor.execute(
                    "UPDATE users SET ban = 1 WHERE user_id = ?", (user_id,)
                )
            except:
                pass

    def unban(self, user_id):
        with self.connection:
            try:
                return self.cursor.execute(
                    "UPDATE users SET ban = 0 WHERE user_id = ?", (user_id,)
                )
            except:
                pass

    def getOffersNumber(self):
        with self.connection:
            res = {"g-m": 0, "a": 0}
            offers = self.cursor.execute("SELECT type FROM last_offers").fetchall()
            for offer in offers:
                if offer[0] == "a":
                    res["a"] += 1
                else:
                    res["g-m"] += 1
            return res

    def getOffersSumm(self):
        with self.connection:
            summ = {"g-m": 0.0, "a": 0.0}
            deals = self.cursor.execute("SELECT * FROM last_offers").fetchall()
            for deal in deals:
                if deal[3] == "a":
                    summ["a"] += getSummFromString(deal[2])
                else:
                    summ["g-m"] += getSummFromString(deal[2])
            return summ

    def get_balance(self, user_id):
        with self.connection:
            res = self.cursor.execute(
                "SELECT `balance` FROM `users` WHERE `user_id` = ?", (user_id,)
            ).fetchone()
            return res

    def set_balance(self, user_id, balance):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `balance` = ? WHERE `user_id` = ?",
                (
                    balance,
                    user_id,
                ),
            )

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
