#Shree Ganeshayah Namah
import win32api
import win32con


class regutil(object):

    def __init__(self):
        self.__ru__openhnd = None
        self.__ru__lasterror = None

    def __openkey(self, pkey=win32con.HKEY_LOCAL_MACHINE, sbkey=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"):
            try:
                retval = win32api.RegOpenKeyEx(pkey, sbkey, 0, win32con.KEY_READ or win32con.KEY_WOW64_64KEY)
                self.__ru__openhnd = retval
                return True
            except Exception, ex:
                self.__ru__lasterror = str(ex)
                return False

    def getregvalue(self, rvalue):
        try:
            retval = win32api.RegQueryValueEx(self.__ru__openhnd, rvalue)
            return retval[0]
        except Exception, ex:
            self.__ru__lasterror = str(ex)
            return False
    
    def getregvalex(self,rvalue,sbkey,pkey = win32con.HKEY_LOCAL_MACHINE):
        if self.__openkey(pkey,sbkey):
            return self.getregvalue(rvalue)
        else:
            return False
             
            

    def getwindowsinfo(self):
        try:
            if self.__openkey(win32con.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"):
                prodid = self.getregvalue('ProductId')
                idate = self.getregvalue('InstallDate')
                prodname = self.getregvalue('ProductName')
                regowner = self.getregvalue('RegisteredOwner')
                regorg = self.getregvalue('RegisteredOrganization')
                return [prodid, idate, prodname, regowner, regorg]
        except Exception, ex:
                self.__ru__lasterror = str(ex)
                return False

    def getlasterror(self):
        if self.__ru__lasterror != None:
            return self.__ru__lasterror
        else:
            return ""

if __name__ == '__main__':
    robj = regutil()
    print robj.getwindowsinfo()
