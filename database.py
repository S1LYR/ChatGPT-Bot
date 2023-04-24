import sqlite3
import time

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def set_time_sub(self, user_id, time_sub):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `time_sub` = ? WHERE `user_id` = ?", (time_sub, user_id,))

    def set_free(self, user_id, Free):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `Free` = ? WHERE `user_id` = ?", (Free, user_id,))

    def get_free(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `Free` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                free = int(row[0])
            return free
    def get_time_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            return time_sub

    def get_sub_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            if time_sub>int(time.time()):
                return True
            else:
                return False

    def set_style(self, user_id, style):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `style` = ? WHERE `user_id` = ?", (style, user_id,))

    def get_style(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `style` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return int(result[0][0])

    def set_language(self, user_id, Language):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `Language` = ? WHERE `user_id` = ?", (Language, user_id,))

    def get_language(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `Language` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return result[0][0]

    def add_check(self, user_id, bill_id):
        with self.connection:
            self.cursor.execute("INSERT INTO `check` (`user_id`, `bill_id`) VALUES (?,?)", (user_id, bill_id,))

    def get_check(self, bill_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `check` WHERE `bill_id` = ?", (bill_id,)).fetchmany(1)
            if not bool(len(result)):
                return False
            return result[0]

    def delete_check(self, bill_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `check` WHERE `bill_id` = ?", (bill_id,))

    def context_check(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `context` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return result[0][0]


    def context_append(self, user_id, context):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `context` = ? WHERE `user_id` = ?", (context, user_id,))
