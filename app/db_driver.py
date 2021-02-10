import sqlite3


class DBDriver:

    def __init__(self, filename):
        self.filename = filename

        try:
            self.connex = sqlite3.connect(self.filename, check_same_thread=False)
        except Exception as e:
            print(e)


    """ (B-1) + (B-2) """
    def get_user(self, username):
        cursor = self.connex.cursor()
        query = """SELECT username, password FROM userCredential WHERE username = ?"""
        query_parameter = (username,)
        data = cursor.execute(query, query_parameter)

        return data.fetchone()


    """ (B-1) + (B-2) """
    def add_user(self, username, password):
        cursor = self.connex.cursor()
        query = """INSERT INTO userCredential(username, password) VALUES (?, ?)"""
        query2 = """INSERT INTO userDeck(username) VALUES (?)"""
        query_parameters = (username, password)
        query2_parameters = (username,)
        data = cursor.execute(query, query_parameters)
        data2 = cursor.execute(query2, query2_parameters)
        self.connex.commit()

        return data, data2

    def get_card(self, ):
        return None
