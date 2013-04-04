#!/bin/python
#Shree Ganeshayah Namah

import xlrd
import types
import csv
from datetime import datetime
########################################################################
class Excelreader(object):
    """
     Utility class to read excel files and return data read
    """ 

    #----------------------------------------------------------------------
    def __init__(self, filename = None):
        """Constructor"""
        self.__er__payload = []
        self.__er__filename = None if filename is None else filename
        self.__er__xlrdwrkobj = None
        self.__er__last__error = None
        
    def setstaticparams(self,filename):
        self.__er__filename = filename
        
    def readexcel(self,sheetno =0,treatcolnoasdate = None):
        try:
            self.__er__payload = []
            if self.__er__filename is None:
                self.__er__last__error = "No Filename Specified,Call setstaticparams with the desired filename"
                return False
            self.__er__xlrdwrkobj = xlrd.open_workbook(self.__er__filename)
            wrksheet = self.__er__xlrdwrkobj.sheet_by_index(sheetno)
            for row in xrange(wrksheet.nrows):        
                    self.__er__payload.append(wrksheet.row_values(row))
            if treatcolnoasdate is not None and type(treatcolnoasdate) == types.ListType:
                for row in self.__er__payload:
                    for datecol in treatcolnoasdate:
                        if type(row[datecol]) in [types.IntType,types.FloatType,types.LongType]:
                            row[datecol] = datetime(*xlrd.xldate_as_tuple(row[datecol], self.__er__xlrdwrkobj.datemode)).strftime("%d-%m-%Y")
            return self.__er__payload        
        except Exception,ex:
            self.__er__last__error = str(ex)
            return False

    def readcsv(self, delimiter=None, quotechar=None):
        try:
            reader_iterator = csv.reader(open(self.__er__filename,"rb"),  delimiter = delimiter if delimiter is not None else ',')
            for row in reader_iterator:
                self.__er__payload.append(row)
            return self.__er__payload
        except Exception,ex:
            self.__er__last__error = str(ex)
            return False


    def getlasterror(self):
        return self.__er__last__error if self.__er__last__error is not None else "Everything Ok"
        
        
        
    
    
