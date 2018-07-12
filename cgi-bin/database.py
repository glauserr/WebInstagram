#! /usr/bin/env python

import MySQLdb
import os
# import socket

class MySQLBase:
    server = "127.0.0.1"
    # server = socket.gethostbyname(socket.gethostname())
    usr = "csci4140"
    pw = "csci4140-2018"
    dbname = "generaldb"
    server_port = 1500
    table = None
    db = None
    cursor = None

    def __init__(self): 
        # Deployment on Openshift MySQL database not working..
        if os.environ.has_key('MYSQL_SERVICE_HOST'):
            self.server = os.environ['MYSQL_SERVICE_HOST']
        if os.environ.has_key('MYSQL_SERVICE_PORT'):
            self.server_port = int(os.environ['MYSQL_SERVICE_PORT'])
        if os.environ.has_key('MYSQL_USER'):
            self.usr = os.environ['MYSQL_USER']
        if os.environ.has_key('MYSQL_PASSWORD'):
            self.pw = os.environ['MYSQL_PASSWORD']
        if os.environ.has_key('MYSQL_DATABASE'):
            self.dbname = os.environ['MYSQL_DATABASE']

        self.db = MySQLdb.connect(host=self.server, port=self.server_port,
                                  user=self.usr, passwd=self.pw,
                                  db=self.dbname)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def exists(self):
        sql = "SHOW TABLES LIKE '%s'" % (self.table) 
        self.cursor.execute(sql)
        if self.cursor.fetchall() == ():
            return False 
        else: 
            return True

    def drop(self):
        sql = "DROP TABLE %s" %(self.table)
        self.cursor.execute(sql)

    def column_names(self, table=None):
        if table is None:
            table = self.table

        sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS \
                WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s'" % (self.dbname, table)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        retList = list()
        for t in data:
            retList.append(t[0])

        return retList

    def in_table(self, column, entry, table=None):
        if self.get_querys_with(column, entry, table):
            return True
        return False

    def get_querys_with(self, column, entry, table=None):
        if table is None:
            table = self.table

        if isinstance(entry, int):
            sql = "SELECT * FROM %s WHERE %s = %d" % (table, column, entry)
        else:
            sql = "SELECT * FROM %s WHERE %s = '%s'" % (table, column, entry)

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert_query(self, columns, values, table=None):
        if table is None:
            table = self.table

        if len(columns) is not len(values):
            return False

        sql = "INSERT INTO %s (" % table

        for i, c in enumerate(columns, 0):
            sql += c
            if i is not len(columns) - 1:
                sql += ","
        sql += ") "

        sql += " VALUES("

        for i, v in enumerate(values, 0):
            if isinstance(v, basestring):
                sql += "'" + v + "'"
            else:
                sql += "'" + str(v) + "'"

            if i != len(values) - 1:
                sql += ","

        sql += ")"

        try:
            self.cursor.execute(sql)
            self.db.commit()

        except:
            self.db.rollback()
            return False

        return True

    def update_query(self, column, with_entry, entry_id, new_entry,
                     isSQLcmd=False):

        sql = "UPDATE %s " % (self.table)

        if isSQLcmd:
            sql += "SET %s = %s " % (entry_id, new_entry)
        elif isinstance(new_entry, int):
            sql += "SET %s = %d " % (entry_id, new_entry)
        else:
            sql += "SET %s = '%s' " % (entry_id, new_entry)

        if isinstance(with_entry, int):
            sql += "WHERE %s = %d " % (column, with_entry)
        else:
            sql += "WHERE %s = '%s' " % (column, with_entry)

        try:
            self.cursor.execute(sql)
            self.db.commit()

        except Exception as err:
            self.db.rollback()
            return False

        return True

    def delete_query(self, column, entry, table=None):
        if table is None:
            table = self.table

        sql = str()

        if isinstance(entry, basestring):
            sql = "DELETE FROM %s WHERE %s='%s'" % (table, column, entry)

        else:
            sql = "DELETE FROM %s WHERE %s=%d" % (table, column, entry)

        try:
            self.cursor.execute(sql)
            self.db.commit()

        except:
            self.db.rollback()
            return False

        return True

    def delete_all(self):
        sql = "DELETE FROM %s" % (self.table)
        try:
            self.cursor.execute(sql)
            self.db.commit()

        except:
            self.db.rollback()
            return False

        return True


class RegisterTable(MySQLBase):
    table = "login_table"
    columns = ("id", "user", "pw", "create_at")

    def create(self):
        sql = """CREATE TABLE login_table(
            id INT NOT NULL AUTO_INCREMENT,
            user VARCHAR(30) NOT NULL,
            pw VARCHAR(50) NOT NULL, 
            create_at DATETIME,
            PRIMARY KEY(id))"""
        try:
            self.cursor.execute(sql)
            self.db.commit()

        except:
            self.db.rollback()
            return False
        return True

    def insert(self, values):
        return self.insert_query(("user", "pw"), values)

    def change_pw(self, user, new_pw):
        return self.update_query("user", user, "pw", new_pw)

    def get_pw(self, user):
        query = self.get_querys_with("user", user)
        return query[0][2]

    def is_registered(self, user):
        if self.get_querys_with("user", user):
            return True
        return False


class AdminTable(RegisterTable):
    table = "admin_table"
    _admin = "admin"
    columns = ("id", "user", "pw", "isinit", "create_at")

    def create(self):
        sql = """CREATE TABLE admin_table(
            id INT NOT NULL AUTO_INCREMENT,
            user VARCHAR(30) NOT NULL,
            pw VARCHAR(100) NOT NULL,
            isinit INT, 
            create_at DATETIME,
            PRIMARY KEY(id))"""
        try:
            self.cursor.execute(sql)
            self.db.commit()

        except:
            self.db.rollback()
            return False
        return True

    def insert(self, values):
        if values[2] == "True":
            values = values[:-1] + ("1",)
        else:
            values = values[:-1] + ("0",)
        return self.insert_query(("user", "pw", "isinit"), values)

    def isinit(self):
        query = self.get_querys_with("user", _admin)
        if query[0][3] == 0:
            return False
        else:
            return True


class SessionTable(MySQLBase):
    table = "session_table"
    columns = ("user", "session_id", "valid_until")

    def create(self):
        sql = """CREATE TABLE session_table(
            user VARCHAR(30) NOT NULL,
            session_id INT NOT NULL,  
            valid_until DATETIME,
            PRIMARY KEY(session_id))"""
        try:
            self.cursor.execute(sql)
            self.db.commit()

        except:
            self.db.rollback()
            return False
        return True

    def in_table(self, column, entry, table=None):
        if self.get_querys_with(column, entry, self.table):
            return True
        return False

    def insert(self, values):
        return self.insert_query(("user", "session_id"), values)

        # user can have multiple ids
    def get_session_ids(self, user):
        querys = self.get_querys_with("user", user, self.table)
        retList = list()
        for q in querys:
            retList.append(q[1])
        return retList

        # id should be unique
    def get_user(self, session_id, table=None):
        query = self.get_querys_with("session_id", session_id, self.table)
        try:
            return query[0][0]
        except:
            return str()

    def sid_is_used(self, session_id):
        return self.in_table("session_id", session_id)

    def delete_session(self, session_id):
        return self.delete_query("session_id", session_id)


class ImageTable(MySQLBase):
    table = "image_table"
    columns = ("id", "user", "link", "date", "public")

    def create(self):
        sql = """CREATE TABLE image_table(
            id  INT NOT NULL AUTO_INCREMENT,
            user VARCHAR(30) NOT NULL,
            link VARCHAR(100) NOT NULL,  
            date DATETIME,
            public TINYINT,
            PRIMARY KEY(id))"""
        try:
            self.cursor.execute(sql)
            self.db.commit()

        except:
            self.db.rollback()
            return False
        return True

    def insert(self, values, public=False):
        values += (int(public),)

        retVal = self.insert_query(("user", "link", "public"), values)
        if retVal:
            retVal = self.update_query(
                "link", values[1], "date", "NOW()", True)

        return retVal

    def get_querys_with(self, column, entry, order):
        if isinstance(entry, int):
            sql = "SELECT * FROM %s WHERE %s = %d "\
                  "ORDER BY %s DESC" % (self.table, column, entry, order)
        else:
            sql = "SELECT * FROM %s WHERE %s = '%s' "\
                  "ORDER BY %s DESC" % (self.table, column, entry, order)

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_image_list(self, user, public, max_number=None):
        select = "SELECT link FROM %s " % (self.table)

        where = ""

        if public != None:
            where = "WHERE %s = %d " % ("public", int(public))

        if user != None:
 
            if where == "":
                where += "WHERE "
            else:
                where += "AND "

            if isinstance(user, int):
                where += "%s = %d " % ("user", user)
            else:
                where += "%s = '%s' " % ("user", user)

        ordered = "ORDER BY %s DESC" % ("date")

        self.cursor.execute(select + where + ordered)

        i = 0
        retList = list()
        if max_number == None:
            while True:
                one_path = self.cursor.fetchone()
                if one_path:
                    retList.append(one_path[0])
                else:
                    break
                i += 1
        else:            
            while(i < max_number):
                one_path = self.cursor.fetchone()
                if one_path:
                    retList.append(one_path[0])
                else:
                    break
                i += 1

        return retList

    def delete_image(self, link):
        return self.delete_query("link", link)
