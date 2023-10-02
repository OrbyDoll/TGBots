import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,)
            )

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)
            ).fetchall()
            return bool(result)

    def get_active_users(self):
        with self.connection:
            return self.cursor.execute(
                "SELECT user_id, nickname, msg_count FROM `users` WHERE `messages` != 'NULL'"
            ).fetchall()

    def set_nickname(self, nickname, user_id):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `nickname` = ? WHERE `user_id` = ?",
                (
                    nickname,
                    user_id,
                ),
            )

    def get_messages(self, user_id):
        with self.connection:
            messages = self.cursor.execute(
                "SELECT `messages` FROM `users` WHERE `user_id` = ?", (user_id,)
            ).fetchall()
            return messages

    def set_messages(self, messages, user_id):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `messages` = ? WHERE `user_id` = ?",
                (
                    messages,
                    user_id,
                ),
            )

    def get_msg_count(self, user_id):
        with self.connection:
            answers = self.cursor.execute(
                "SELECT `msg_count` FROM `users` WHERE `user_id` = ?", (user_id,)
            ).fetchall()
            return answers

    def set_msg_count(self, msg_count, user_id):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `msg_count` = ? WHERE `user_id` = ?",
                (
                    msg_count,
                    user_id,
                ),
            )
    def clearall(self):
        with self.connection:
            return self.cursor.execute("DELETE FROM `users`")