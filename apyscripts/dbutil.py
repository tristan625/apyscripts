# Shree Ganeshaayah Namah
__author__ = 'aditya'
#import importlib


class dbutil(object):
    def __init__(self, dbtype):
        self.dbcon = None
        self.dbcursor = None
        self.dbhost = None
        self.dbuser = None
        self.dbpass = None
        self.dbname = None
        self.dbport = None
        self.db_types_supported = {'mysql': 'MySQLdb', 'pgsql': 'psycopg2', 'sqlite': 'sqlite3'}
        self.dbtype = dbtype
        self.last_error = None
        if not self.dbtype in self.db_types_supported:
            raise NotImplementedError("Invalid Or NotImplemented DB Type Specified")
        try:
            adapter = self.db_types_supported[self.dbtype]
            self.db = __import__(adapter, globals(), locals(), [], -1)
            #self.db = importlib.import_module(adapter)
        except ImportError, ex:
            raise ImportError("Unable To Import DbAdapter %s" % adapter)

    def set_connection_params(self, db, host=None, user=None, passwd=None, port=None):
        self.dbhost = host
        self.dbuser = user
        self.dbpass = passwd
        self.dbname = db
        try: 
            self.dbport = int(port)
        except ValueError, ve:
            self.last_error = str(ve)
            self.dbport = None
        

    def getinsertsql(self, tblname, fields, values=None, makeprepared=True):
        counter = 0
        stmt = "insert into %s" % tblname
        stmt += "("
        for field in fields:
            stmt += field + ","
        stmt = stmt[:-1]
        stmt += ") values("
        for field in fields:
            counter += 1
            stmt += "%s," if self.db.paramstyle == 'pyformat' or self.db.paramstyle == "format" else "?," \
                if self.db.paramstyle == 'qmark' else ':' + str(counter) + ','
        stmt = stmt[:-1]
        stmt += ")"
        return stmt

    def getupdatesql(self, tblname, fields, wherecl, values=None, makeprepared=True):
        counter = 0
        stmt = "update %s set " % tblname
        for cnt in range(len(fields)):
            stmt += " %s=%s" % (fields[cnt],
                                "%s," if self.db.paramstyle == 'pyformat' or self.db.paramstyle == "format" else "?,"
                                if self.db.paramstyle == 'qmark' else ':' + str(counter) + ',')
        stmt = stmt[:-1]
        stmt += " where %s" % wherecl
        return stmt


    def querydb(self, stmt, args=None, closecon=True):
        try:
            if self.dbcon is None or (hasattr(self.dbcon,'open') and self.dbcon.open == 0) or (hasattr(self.dbcon, 'closed') and self.dbcon.closed ==1):
                if not self.__dbconnect():
                    raise Exception, "Unable To Connect To DB:-%s" % self.last_error
            self.dbcursor = self.dbcon.cursor()
            self.dbcursor.execute(stmt, args if args is not None and (
                isinstance(args, dict) or isinstance(args, list)) else None)
            return self.dbcursor.fetchall()
        except Exception, ex:
            self.last_error = str(ex)
            return False
        finally:
            if self.dbcursor is not None: self.dbcursor.close()
            if self.dbcon is not None and closecon: self.dbcon.close()


    def __dbconnect(self):
        try:
            if self.dbtype != "sqlite":
                if self.dbport is None:
                    if self.dbtype == "mysql":
                        self.dbcon = self.db.connect(host="%s" % self.dbhost, user="%s" % self.dbuser, passwd="%s" % self.dbpass,
                                                     db="%s" % self.dbname)
                    else:
                        self.dbcon = self.db.connect(host="%s" % self.dbhost, user="%s" % self.dbuser, password="%s" % self.dbpass,
                                                     database="%s" % self.dbname)
                else:
                    if self.dbtype == "mysql":
                        self.dbcon = self.db.connect(host="%s" % self.dbhost, user="%s" % self.dbuser, passwd="%s" % self.dbpass,
                                                     db="%s" % self.dbname, port=self.dbport)
                    else:
                        self.dbcon = self.db.connect(host="%s" % self.dbhost, user="%s" % self.dbuser, password="%s" % self.dbpass,
                                                     database="%s" % self.dbname, port=self.dbport)
            else:
                self.dbcon = self.db.connect(self.dbname)
            return True
        except Exception, ex:
            self.last_error = str(ex)
            return False

    def __pushid(self, args):
        for cnt in range(len(args)):
            if args[cnt] == "@@id":
    #            we need to replace this the last inserted id
                 args[cnt] = self.dbcursor.lastrowid
        return args

    def execute_batch(self, stmt_dict):
        try:
            if self.dbcon is None or (hasattr(self.dbcon,'open') and self.dbcon.open == 0) or (hasattr(self.dbcon, 'closed') and self.dbcon.closed ==1):
                if not self.__dbconnect():
                    raise Exception, "Unable To Connect To DB:-%s" % self.last_error
            self.dbcon.autocommit = False
            self.dbcursor = self.dbcon.cursor()
            for stmt in stmt_dict:
                self.dbcursor.execute(stmt, stmt_dict[stmt] if stmt_dict[stmt] is not None else None )
            self.dbcon.commit()
            return True
        except Exception, ex:
            self.last_error = str(ex)
            if self.dbcon is not None:
                self.dbcon.rollback()
            return False
        finally:
            if self.dbcursor is not None:
                self.dbcursor.close()
            if self.dbcon is not None:
                self.dbcon.autocommit = True
            if self.dbcon is not None:
                self.dbcon.close()


    def get_last_error(self):
        return self.last_error if self.last_error is not None else "Everything Ok"


if __name__ == '__main__':
    dbobj = dbutil('mysql')
    dbobj.set_connection_params("192.168.1.8", "activedb_user", "meenakshi", "activedb")
    retval = dbobj.querydb("select * from activation where serialno=%(serial)s", {'serial': '009110435'})
    print(retval)    
