import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        with self.connection:
            offers = self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS offers(
                    owner_id INTEGER,
                    products TEXT);
                """
            )
            temp_offers = self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS temp_offers(
                    owner_id TEXT,
                    products TEXT);
                """
            )
            users = self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER,
                    garant_balance INTEGER,
                    nickname TEXT);
                """
            )
            return offers, users

    def add_user(self, user_id, garant_balance, nickname):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `users` (`user_id`, `garant_balance`, `nickname`) VALUES (?,?,?)",
                (user_id, garant_balance, nickname),
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

    def get_user_from_nick(self, nick):
        with self.connection:
            res = self.cursor.execute(
                "SELECT * FROM `users` WHERE `nickname` = ?", (nick,)
            ).fetchone()
            return res

    def get_all_offers(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `offers`").fetchall()

    def get_user_offers(self, user_id):
        with self.connection:
            res = self.cursor.execute(
                "SELECT `products` FROM `offers` WHERE `owner_id` = ?", (user_id,)
            ).fetchone()
            return res

    def insert_offer_owner(self, user_id):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `offers` (`owner_id`, `products`) VALUES (?,?)",
                (
                    user_id,
                    "",
                ),
            )

    def add_offer(self, user_id, offer: list):
        with self.connection:
            prev_offers = self.get_user_offers(user_id)[0]
            new_offers = prev_offers + "/" + offer[0] + "_" + offer[1] + "_" + offer[2]
            return self.cursor.execute(
                "UPDATE `offers` SET `products` = ? WHERE `owner_id` = ?",
                (
                    new_offers,
                    user_id,
                ),
            )

    def del_offer_products(self, user_id, del_offer: list):
        with self.connection:
            prev_offers = self.get_user_offers(user_id)[0]
            offer_str = "/" + del_offer[0] + "_" + del_offer[1] + "_" + del_offer[2]
            new_offers = prev_offers.replace(offer_str, "")
            return self.cursor.execute(
                "UPDATE `offers` SET `products` = ? WHERE `owner_id` = ?",
                (
                    new_offers,
                    user_id,
                ),
            )

    def set_balance(self, user_id, balance):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `garant_balance` = ? WHERE `user_id` = ?",
                (
                    balance,
                    user_id,
                ),
            )

    def update_price(self, user_id, offer_str, new_price):
        prev_offers = self.get_user_offers(user_id)[0]
        offer_str = offer_str.replace("/", "_")
        offer_str_split = offer_str.split("_")
        new_offers = prev_offers.replace(
            offer_str, f"{offer_str_split[0]}_{offer_str_split[1]}_{new_price}"
        )
        with self.connection:
            return self.cursor.execute(
                "UPDATE `offers` SET `products` = ? WHERE `owner_id` = ?",
                (
                    new_offers,
                    user_id,
                ),
            )

    def insert_owner_temp(self, user_id):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `temp_offers` (`owner_id`, `products`) VALUES (?,?)",
                (
                    user_id,
                    "",
                ),
            )

    def get_user_tempOffers(self, user_id):
        with self.connection:
            res = self.cursor.execute(
                "SELECT `products` FROM `temp_offers` WHERE `owner_id` = ?", (user_id,)
            ).fetchone()
            return res

    def add_tempOffer(self, user_id, offer: list):
        with self.connection:
            prev_offers = self.get_user_tempOffers(user_id)[0]
            new_offers = prev_offers + "/" + offer[0] + "_" + offer[1] + "_" + offer[2]
            return self.cursor.execute(
                "UPDATE `temp_offers` SET `products` = ? WHERE `owner_id` = ?",
                (
                    new_offers,
                    user_id,
                ),
            )

    def del_tempOffer_products(self, user_id, del_offer: list):
        with self.connection:
            prev_offers = self.get_user_tempOffers(user_id)[0]
            offer_str = "/" + del_offer[0] + "_" + del_offer[1] + "_" + del_offer[2]
            new_offers = prev_offers.replace(offer_str, "")
            return self.cursor.execute(
                "UPDATE `temp_offers` SET `products` = ? WHERE `owner_id` = ?",
                (
                    new_offers,
                    user_id,
                ),
            )

    def get_all_tempOffers(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `temp_offers`").fetchall()

    def get_all_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users").fetchall()

    def stats(self, offers_number):
        with self.connection:
            users = self.get_all_users()
            msg = (
                "❕ Информация:\n\n❕ Пользователей в боте - "
                + str(len(users))
                + "\n❕ Проведено сделок - "
                + str(offers_number["g-m"])
            )
            return msg
