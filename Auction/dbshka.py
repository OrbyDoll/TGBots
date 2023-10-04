import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        with self.connection:
            auct = self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS auctions(
                    auction_id INTEGER PRIMARY KEY,
                    members INTEGER NOT NULL DEFAULT 0,
                    start_cost INTEGER,
                    author_id INTEGER,
                    product TEXT,
                    current_cost INTEGER,
                    status TEXT DEFAULT 'inactive',
                    members_id TEXT DEFAULT '',
                    category TEXT,
                    description TEXT,
                    autostart INTEGER DEFAULT 0);
                """
            )
            users = self.cursor.execute(
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

    def get_auction(self, author_id):
        with self.connection:
            res = self.cursor.execute(
                "SELECT * FROM `auctions` WHERE `author_id` = ?", (author_id,)
            ).fetchone()
            return res

    def add_auction(self, author_id, product, start_cost, category, description):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `auctions` (`author_id`, `product`, `start_cost`, `current_cost`, `category`, `description`) VALUES (?,?,?,?,?,?)",
                (author_id, product, start_cost, start_cost, category, description),
            )

    def del_auction(self, author_id):
        with self.connection:
            return self.cursor.execute(
                "DELETE FROM `auctions` WHERE `author_id` = ?", (author_id,)
            )

    def check_active_auction(self, author_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `auction_id` FROM `auctions` WHERE `author_id` = ?",
                (author_id,),
            ).fetchall()
            return bool(result)

    def set_start_cost(self, author_id, new_start_cost):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `auctions` SET `start_cost` = ? WHERE `author_id` = ?",
                (
                    new_start_cost,
                    author_id,
                ),
            )

    def get_all_auctions(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `auctions`").fetchall()

    def get_auction_members(self, author_id):
        with self.connection:
            return self.cursor.execute(
                "SELECT `members` FROM `auctions` WHERE `author_id` = ?", (author_id,)
            ).fetchone()

    def change_members(self, author_id, factor):
        with self.connection:
            actual_members = self.get_auction_members(author_id)[0]
            new_members = actual_members + 1 * factor
            return self.cursor.execute(
                "UPDATE `auctions` SET `members` = ? WHERE `author_id` = ?",
                (
                    new_members,
                    author_id,
                ),
            )

    def get_members_id(self, author_id):
        with self.connection:
            res = self.cursor.execute(
                "SELECT `members_id` FROM `auctions` WHERE `author_id` = ?",
                (author_id,),
            ).fetchone()
            return res

    def set_members_id(self, author_id, new_members_id):
        with self.connection:
            self.cursor.execute(
                "UPDATE `auctions` SET `members_id` = ? WHERE `author_id` = ?",
                (
                    new_members_id,
                    author_id,
                ),
            )

    def set_auction_status(self, author_id, status):
        with self.connection:
            res = self.cursor.execute(
                "UPDATE `auctions` SET `status` = ? WHERE `author_id` = ?",
                (
                    status,
                    author_id,
                ),
            )

    def set_current_cost(self, author_id, cost):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `auctions` SET `current_cost` = ? WHERE `author_id` = ?",
                (
                    cost,
                    author_id,
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

    def set_autostart(self, user_id, members):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `auctions` SET `autostart` = ? WHERE `author_id` = ?",
                (members, user_id),
            )

    def get_autostart(self, user_id):
        with self.connection:
            res = self.cursor.execute(
                "SELECT `autostart` FROM `auctions` WHERE `author_id` = ?", (user_id,)
            ).fetchone()
            print(res, "autostart")
            return res
