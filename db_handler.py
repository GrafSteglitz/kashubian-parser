"""
@module
"""
# from dataclasses import dataclass, field
import re
from db_connect import DBConnection


# @dataclass
class DBHandler:
    """
    An interface for managing database queries initiated by Tokenizer.
    Connects to database using DBConnect.
    """
    # db_matches: dict = field(init=False)
    def __init__(self):
        self.db_matches = {}

    def _check_morph_with_db(self, query):
        """
        Look up a morphological form in the database.
        :param query: str query to be looked up
        :return:
        """

        # makes sure the word is not too short, in which case some extensive and unhelpful data will be returned
        if len(query) > 2:
            # check if the morphological form has already been found and stored
            if query in self.db_matches:
                db_match_attrs = self.db_matches[query]
                return
            db_match_attrs = self.get_attrs_from_db(query)
            if not db_match_attrs:
                return
            match_record = {query: db_match_attrs}
            if query not in self.db_matches:
                self.db_matches.update(match_record)

    def get_attrs_from_db(self, query, table='DICT', col='LEXEME'):
        """

        :param col: col in db table to search
        :param table: table in db to search
        :param query: string to search in db, '%' is appended
        :return: a list of unique attrs
        """
        match_attrs = []
        db_lexeme_match = self.db_lookup(table, col, query + '.*')
        db_results_dict_list = []

        if db_lexeme_match:
            #  and len(db_lexeme_match) == 1
            for entry in db_lexeme_match:
                db_results_dict = {'lexeme': entry[0], 'attrs': entry[1]}
                db_results_dict_list.append(db_results_dict)
            match_attrs = [a['attrs'] for a in db_results_dict_list]
            match_attrs = list(set(match_attrs))
            # print(match_attrs)
            # only returns attrs if one results is found
            if len(match_attrs) == 1:
                match_attrs = [a for a in re.split(r":", match_attrs[0]) if a]

        return match_attrs

    @staticmethod
    def db_lookup(table, column, query):
        """

        :param table:
        :param column:
        :param query:
        :return:
        """
        db = DBConnection()
        output = db.search(table, column, query)
        db.close()
        return output
