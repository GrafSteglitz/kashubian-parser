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
        self.conn = None
        self.cur = None
        try:
            self.conn = psycopg2.connect(database=self.db, user=self.db_user, password=self.db_pass, host=self.db_host,
                                         port=self.db_port)
            self.cur = self.conn.cursor()
            logging.info("Opened database successfully")
        except DatabaseError as db_err:
            logging.error(f"Database error: {db_err}")

    def close(self):
        """

        :return:
        """
        if self.conn:
            self.conn.close()


    def search(self, table, column, s_term):
        """

        :param table:
        :param column:
        :param s_term:
        :return:
        """
        from psycopg2 import sql
        q = sql.SQL("SELECT * FROM {} WHERE {} ~* %s").format(
            sql.Identifier(table),
            sql.Identifier(column)
        )

        if not self.cur:
            return []
        try:
            self.cur.execute(q, (s_term,))

        except DatabaseError as db_err:
            print(f'Error executing query: {db_err}')
            return []

        rows = self.cur.fetchall()

        print("Operation done successfully")
        return rows

    def insert_records(self, in_set):
        remove_set = {''}
        for word in in_set:
            self.cur.execute("SELECT * FROM FORMS WHERE FORM = %s", (word,))
            rows = self.cur.fetchall()
            if rows:
                if rows[0][0] == word:
                    remove_set.add(word)
        for w in in_set:
            if w not in remove_set:
                self.cur.execute("INSERT INTO FORMS (FORM) VALUES (%s)", (w,))
        self.conn.commit()
        print("Records created!")

    def update_records(self):
        pass

    def find_adjectives(self, search):
        self.cur.execute("SELECT * FROM FORMS WHERE FORM LIKE %s", (search,))

    def tag_records(self):
        self.cur.execute("SELECT * FROM FORMS;")
        rows = self.cur.fetchall()
        for r in rows:
            w = Word(r[0])
            if w.is_adjective():
                self.cur.execute(
                    "UPDATE FORMS SET ATTRS = 'adj' WHERE ID = %s", (w.root,)
                )
                self.conn.commit()


if __name__ == '__main__':
    db = DBConnection()
    db.tag_records()
    # a = db.extract_set("./Texts/Ana_pure_text.txt")
    # db.insert_records(a)
    db.close()
