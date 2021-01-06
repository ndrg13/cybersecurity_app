import sqlite3


class DBDriver:
    filename = None

    def __init__(self, filename):
        self.filename = filename

    def connect(self):
        return sqlite3.connect(self.filename)

    def get_user(self, username):
        connex = self.connect()
        cursor = connex.cursor()
        data = cursor.execute("""SELECT username, password FROM userCredential WHERE username = ?""", (username,))

        return data.fetchone()

    def add_user(self, username, password):
        connex = self.connect()
        cursor = connex.cursor()
        data = cursor.execute("""INSERT INTO userCredential(username, password) VALUES (?, ?)""", (username, password))
        connex.commit()

        return data



