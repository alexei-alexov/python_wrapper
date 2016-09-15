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
        sql = "SELECT %s FROM %s" % (", ".join(fields), tables if isinstance(tables, str) else ", ".join(tables))

        # add condition part is nessesary
        if condition is not None:
            sql += " WHERE " + condition
        # same with group by
        if groupby is not None:
            sql += " SORT BY " + ",".join(groupby)
        # and with order by
        if orderby is not None:
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

        Return True if everything ok
        """
        sql = "UPDATE " + table +\
            " SET " + set +\
            (" WHERE " + where) if where is not None else ""

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

    def insert(self, table, fields, values):
        """
        This method provides delete SQL command [OK]

        Args:
            table  (str): Name of table.
            fields (tuple): Tuple with name of insert fields.
            values (tuple): Insert row should always be a tuple

        Return:
            id (int): generated identifier of new object
            -1 if error of execution
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

    def close(self):
        self.connect.close()


class WrongData(Exception):
    """
    This exception raise when trying to modify data that is not in table
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
