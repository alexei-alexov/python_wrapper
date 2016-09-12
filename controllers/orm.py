"""
This module contains wrapper to work with database
"""

import MySQLdb
import json


class Wrapper(object):
    """
    This class provide basic work with database
    """


    def __init__(self, config):
        """
        Initialize new database connection with dict of parameters
        """
        
        self.debug = config["debug"]
        if self.debug:
            print "Debug mode active"
        print config
        
        self.connect = MySQLdb.connect(config["host"], config["user"], config["passwrd"], config["db"])


    def select(self, tables, fields, condition=None, orderby=None, groupby=None):
        """
        This method provides select SQL command
        """
        sql = "SELECT %s FROM %s" % (", ".join(fields), ", ".join(tables))

        # add condition part is nessesary
        if not condition is None:
            sql += " WHERE " + condition
        # same with group by
        if not groupby is None:
            sql += " SORT BY " + ",".join(groupby)
        # and with order by
        if not orderby is None:
            sql += " ORDER BY " + ",".join(orderby)

        if self.debug:
            print sql

        cursor = self.connect.cursor()

        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception, exept:
            print exept


    def update(self, table, set, where=None):
        """
        This method provide update SQL command
        """
        sql = "UPDATE " + table +\
                " SET " + set +\
                (" WHERE " + where) if not where is None else ""

        cursor = self.connect.cursor()

        try:
            cursor.execute(sql)
            self.connect.commit()
            return True
        except Exception, exept:
            print exept
            self.connect.rollback()
            return False


    def insert(self, table, fields, values):
        """
        This method provides delete SQL command [OK]

        Args:
            table  (str): Name of table.
            fields (tuple): Tuple with name of insert fields.
            values (tuple): Insert row should always be a tuple
                
        Return:
            id (int): generated identifier of new object if -1 error of execution
        """
        
        sql = "INSERT INTO " + table +\
                str(tuple(fields)).replace("\'", "") + " VALUES " +\
                str(values)

        if self.debug:
            print sql

        cursor = self.connect.cursor()

        try:
            cursor.execute(sql)
            self.connect.commit()
            return cursor.lastrowid
        except Exception, exept:
            print exept
            self.connect.rollback()
            return -1


    def delete(self, table, condition):
        """
        This method provides delete SQL method
        """
        sql = "DELETE FROM %s WHERE %s"\
            % (table, condition)

        if self.debug:
            print sql

        cursor = self.connect.cursor()

        try:
            cursor.execute(sql)
            self.connect.commit()
            return True
        except Exception, exept:
            print exept
            self.connect.rollback()
            return False


if __name__ == "__main__":
    wrapper = Wrapper(json.load(open("config.json", "r")))
    #wrapper.insert("users", ("firstname", "lastname", "email"), [("Viktor", "Viktorovich", "v@gmail.com"), ("Viktor2", "Viktorovich", "v@gmail.com")])
    #wrapper.insert("posts", ("user_id", "text"), [(1, "text1"), (1, "text2")])
    #wrapper.update("posts", "text = 'new text'", "id = 1")
    #wrapper.delete("posts", "id = 2")
    #print wrapper.select(["posts"], "*")
