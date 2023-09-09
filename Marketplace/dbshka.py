import sqlite3

class Database():
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
    def create_tables(self):
        with self.connection:
            auct = self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS offers(
                    owner_id INTEGER,
                    products TEXT);
                """
            )
            users =  self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER,
                    garant_balance INTEGER,
                    nickname TEXT);
                """
            )
            return auct, users
    def add_user(self, user_id, garant_balance, nickname):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `users` (`user_id`, `garant_balance`, `nickname`) VALUES (?,?,?)", (user_id,garant_balance, nickname)
            )

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)
            ).fetchall()
            return bool(result)
    def get_user(self, user_id):
        with self.connection:
            res = self.cursor.execute(
                "SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)
            ).fetchone()
            return res
    def get_all_offers(self):
        with self.connection:
            return self.cursor.execute(
                "SELECT * FROM `offers`"
            ).fetchall()
    def get_user_offers(self, user_id):
        with self.connection:
            res = self.cursor.execute(
                "SELECT `products` FROM `offers` WHERE `owner_id` = ?", (user_id,)
            ).fetchone()
            return res
    def insert_offer_owner(self,user_id):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `offers` (`owner_id`, `products`) VALUES (?,?)", (user_id,'',)
            )
    def add_offer(self, user_id, offer:list):
        with self.connection:
            prev_offers = self.get_user_offers(user_id)[0]
            new_offers = prev_offers + '/' + offer[0] + '_' + offer[1] + '_' + offer[2]
            return self.cursor.execute(
                "UPDATE `offers` SET `products` = ? WHERE `owner_id` = ?", (new_offers, user_id,)
            )
    def del_offer_products(self, user_id, del_offer:list):
        with self.connection:
            prev_offers = self.get_user_offers(user_id)[0]
            offer_str = '/' + del_offer[0] + '_' + del_offer[1] + '_' + del_offer[2]
            new_offers = prev_offers.replace(offer_str,'')
            print(offer_str, 'no')
            return self.cursor.execute(
                "UPDATE `offers` SET `products` = ? WHERE `owner_id` = ?", (new_offers, user_id,)
            )
    def set_balance(self, user_id, balance):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `garant_balance` = ? WHERE `user_id` = ?", (balance, user_id,) 
            )
