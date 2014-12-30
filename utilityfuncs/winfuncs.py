#Shree Ganeshayah Namah

from win32api import GetSystemDirectory,GetTempPath, GetModuleFileName,GetModuleHandle
from win32gui import FindWindow
import win32con
from os.path import dirname


def isAppRunning(apptitle=None,appclass=None):
     try:
         return FindWindow(appclass,apptitle)
     except Exception,ex:
         return 0

def getapppath(returnpathwexe=False):
    if not returnpathwexe:
        return dirname(GetModuleFileName(GetModuleHandle(None)))
    else:    
        return GetModuleFileName(GetModuleHandle(None))

def getSysDir():
    return GetSystemDirectory()

def getTempDir():
    return GetTempPath()

