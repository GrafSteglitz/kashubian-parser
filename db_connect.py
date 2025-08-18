"""
@module
"""
import os
import logging
import psycopg2
from psycopg2 import DatabaseError
from IgnoreFiles.word import Word


class DBConnection:
    """A class to create a connection to the morphology database."""
    def __init__(self):

        self.db = os.getenv('db')
        self.db_user = os.getenv('db_user')
        self.db_pass = os.getenv('DB_PASS')
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        try:
            self.conn = psycopg2.connect(database=self.db, user=self.db_user, password=self.db_pass, host=self.db_host,
                                         port=self.db_port)
        except DatabaseError as db_err:
            logging.error(f"Database error: {db_err}")

        logging.info("Opened database successfully")
        self.cur = self.conn.cursor()

    def close(self):
        """

        :return:
        """
        self.conn.close()


    def search(self, table, column, s_term):
        """

        :param table:
        :param column:
        :param s_term:
        :return:
        """
        q = "SELECT * FROM " + table + " WHERE " + column + " ~* '" + s_term + "';"

        try:
            self.cur.execute(q)

        except DatabaseError as db_err:
            print(f'Error executing query: {db_err}')
            return []

        rows = self.cur.fetchall()

        print("Operation done successfully")
        return rows

    def insert_records(self, in_set):
        remove_set = {''}
        for word in in_set:
            select_q = "SELECT * FROM FORMS WHERE FORM = '" + word + "'"
            self.cur.execute(select_q)
            rows = self.cur.fetchall()
            if rows:
                if rows[0][0] == word:
                    remove_set.add(word)
        for w in in_set:
            if w not in remove_set:
                q = "INSERT INTO FORMS (FORM) VALUES ('" + w + "')"
                self.cur.execute(q)
        # rows = cur.fetchall()
        self.conn.commit()
        print("Records created!")

    def update_records(self):
        pass

    def find_adjectives(self, search):
        select_q = "SELECT * FROM FORMS WHERE FORM LIKE '" + search + "'"
        self.cur.execute(select_q)
        pass

    def tag_records(self):
        q = "SELECT * FROM FORMS;"
        self.cur.execute(q)
        rows = self.cur.fetchall()
        for r in rows:
            w = Word(r[0])
            if w.is_adjective():
                uq = "UPDATE FORMS set ATTRS = \'adj\' where ID LIKE " + w.root
                self.cur.execute(uq)
                self.conn.commit()


if __name__ == '__main__':
    db = DBConnection()
    db.tag_records()
    # a = db.extract_set("./Texts/Ana_pure_text.txt")
    # db.insert_records(a)
    db.close()
