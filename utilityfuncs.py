#Shree Ganeshayah Namah

import types,os,os.path,socket,glob,zipfile,sys,datetime,win32api,csv
from win32api import GetSystemDirectory,GetTempPath, GetModuleFileName,GetModuleHandle
from win32gui import FindWindow
failure_reason=None

def issequence(seq):
   if type(seq)==types.ListType or type(seq)==types.TupleType:
        return True
   else:
        return False

def join(seq,sep):
    retstr=""
    if type(seq)==types.ListType or type(seq)==types.TupleType and type(sep)==types.StringType:
        for elem in seq:
            if not type(elem)==types.StringType:
                retstr+=str(elem)+sep
            else:
                retstr+=elem+sep
        return retstr[:len(retstr)-1]
    else:
        return ""

def isAppRunning(apptitle=None,appclass=None):
     try:
         return FindWindow(appclass,apptitle)
     except Exception,ex:
         return 0
def getapppath(returnpathwexe=False):
    if not returnpathwexe:
        return os.path.dirname(GetModuleFileName(GetModuleHandle(None)))
    else:    
        return GetModuleFileName(GetModuleHandle(None))

def findmyini(path,ext="ini"):
    resultset=searchfiles(path,"*.%s" % ext)
    if len(resultset)==0:
        return None
    else:
        return resultset[0]

def searchfiles(spath,pattern):
   if not spath.endswith("\\"):
       spath=spath + "\\"
   spattern=spath+pattern
   return glob.glob(spattern)

def getlasterror():
    return failure_reason

def modifyini(fname, keyvalues, commentchar='*'):
    """
    Utility function to modify keyword values as per the value
    specified for a keyword in the keyvalues dict
    """
    try:
        lines_to_write = []
        if not os.path.exists(fname):
            failure_reason = "Invalid File Specified"
            return False
        fp = open(fname)
        lines = fp.readlines()
        fp.close()
        for line in lines:
            line = line.strip().lower()
            print line
            if line.startswith(commentchar): ## This is a comment so skip it
                lines_to_write.append(line + os.linesep)
                continue
            for key in keyvalues:
                if line.find('=') == -1:
                    # invlaid line of some sort i.e. it is 
                    # not a comment line and does not contain
                    # a keyword
                    break
                keyword = line.split("=")[0].strip()
                value = line.split("=")[1].strip()
                print keyword, value
                if keyword in keyvalues:
                    line = line[:line.rfind("=") + 1] + keyvalues[keyword] + os.linesep        
            if not line.endswith(os.linesep):
                line = line + os.linesep        
            lines_to_write.append(line)        
        fp = open(fname, 'w')
        print lines_to_write
        fp.writelines(lines_to_write)
        fp.close()
        return True
    except Exception, ex:
        print str(ex)
        failure_reason = str(ex)
        return False
        
    
def parseini(fname,keys,commentchar):
        """Utility function for fetching values from Payman style *.ini files
        Return:-Dict conatining values for keys passed or empty dict if values
        not found
        """
        valuedict=dict()
        if os.path.exists(fname):
            fp=open(fname)
            lines=fp.readlines()
            fp.close()
            for line in lines:
                line=line.strip().lower()
                if type(commentchar) == types.ListType:
                    if True in map(line.startswith,commentchar): ## This is a comment so skip it
                        continue
                else:
                    if line.startswith(commentchar):## This is a comment so skip it
                        continue
                for key in keys:
                    if line.startswith(key):
                        valuedict[key]=line.split("=")[1].strip()
            return valuedict
        else:
            return valuedict

def convert(matter):
    res=""
    if type(matter)in[types.StringType,types.StringTypes]:
        for i in matter:
            if ord(i) not in [32,10,13]:
                i=chr(256-ord(i))
            res+=i
    else:
        res=chr(256-ord(str(matter)))
    return res

def deconvert(matter):
    res=""
    for i in matter:
        if ord(i) not in [32,10,13,44]:
            i=chr(256-ord(i))
        res+=i
    return res

def mdcompress(data,cmptype):
    data=data.strip()
    mdatalen=len(data)
    mctr=1
    mtemp1=0
    mretdata=0
    mrettemp=''
    for i in range(mdatalen):
        mtemp=ord(data[i:i+1])
        mretdata=mtemp
        if cmptype==0:
            mtemp1= 57
        else:
            mtemp1=64
        mv1=int(self.mretnum(mctr,cmptype))
        mtemp1+= mctr + mv1
        mtemp+=-mtemp1
        mretdata+=-mtemp1
        mrettemp+=chr(mretdata)

        if cmptype==0:
            if mctr==9:
                mctr=1
            else:
                mctr+=1
        else:
            if mctr==6:
                mctr=1
            else:
                mctr+=1
    mretdata=mrettemp
    return str(mretdata)

def getIp():
    try:
        import socket
        ip=socket.gethostbyname(socket.gethostname())
        return ip
    except ImportError,ie:
       return False

def getSysDir():
    return GetSystemDirectory()
def getTempDir():
    return GetTempPath()
def checkzip(fname):
    zipobj=zipfile.ZipFile(fname,"r")
    if zipobj.testzip() is None:
        return True
    else:
        return False

def createzip(fname,files,basedir):
    try:
        origdir=os.getcwd()
        if basedir.endswith("\\"):
            basedir=basedir[:-1]
        zipobj=zipfile.ZipFile(fname,"w")
        for file in files:
            if os.path.exists(basedir+ "\\" + file):
                if os.path.isfile(basedir+ "\\" + file):
                    os.chdir(basedir)
                    zipobj.write(file)
                    #os.chdir(os.path.split(file)[0])
                    #zipobj.write(os.path.split(file)[1])
                    os.chdir(origdir)
                if os.path.isdir(basedir+ "\\" + file):
                    createzip(fname,os.listdir(basedir+ "\\" + file),basedir)
        zipobj.close()
        return True
    except IOError,ie:
        print str(ie)
        failure_reason=str(ie)
        return False
def argltodict(arglist):
   argdict = {}
   for opt,val in arglist:
       argdict[opt]= val
   return argdict    
def getwindowsinfo():
       pass
      ##win32api.RegOpenKeyEx()
##def getwindowsinfo():
##   hkey=None
##   hsubkey=None
##   fp=open("rlog.txt","w")
##   try:
##        import _winreg
##        hkey=_winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
##        hsubkey=_winreg.OpenKeyEx(hkey,"SOFTWARE\Microsoft\Windows NT\CurrentVersion",0,_winreg.KEY_READ)
##        winserial=_winreg.QueryValueEx(hsubkey,"ProductId")[0]
##        fp.write(winserial)
##        widate=_winreg.QueryValueEx(hsubkey,"InstallDate")[0]
##        prodname=_winreg.QueryValueEx(hsubkey,"ProductName")[0]
##        fp.write(prodname)
##        widate=str(datetime.datetime.fromtimestamp(widate))
##        fp.write(str(widate))
##        worg=_winreg.QueryValueEx(hsubkey,"RegisteredOrganization")[0]
##        wowner=_winreg.QueryValueEx(hsubkey,"RegisteredOwner")[0]
##        if worg==None or len(worg)==0:
##            worg="NA"
##        fp.write(str(worg))
##        return [winserial,widate,prodname]
##   except ImportError,ie:
##        failure_reason=str(ie)
##        fp.write(str(ie))
##        return False
##   except EnvironmentError,er:
##       failure_reason=str(er)
##       fp.write(str(er))
##       return False
##   except Exception,ex:
##       failure_reason=str(ex)
##       fp.write(ex)
##       return False
##   finally:
##       if hsubkey:
##           _winreg.CloseKey(hsubkey)
##       if hkey:
##           _winreg.CloseKey(hkey)
##       fp.close()
def dumptocsv(payload,headers,ofname):
    try:
        f=open(ofname,"wb")
        wobj=csv.writer(f)
        wobj.writerow(headers)
        wobj.writerows(payload)
        f.close()
        return True
    except IOError,ex:
        failure_reason=str(ex)
        return False
    except Exception,ex:
        failure_reason=str(ex)
        return False
#def dumptoexcel(payload,headers,ofname):
#        try:
#            wrkbook=xlwt.Workbook()
#            wrksheet=wrkbook.add_sheet("Sheet 1")
#            wrkbook.set_active_sheet(0)
#            rowno=0
#            for cnt in range(len(headers)):
#                wrksheet.write(rowno,cnt,headers[cnt])
#            rowno+=1
#            for row_to_write in payload:
#                #row_to_write=payload[index]
#                for cell in range(len(row_to_write)):
#                    wrksheet.write(rowno,cell,row_to_write[cell])
#                rowno+=1
#            wrkbook.save(ofname)
#            return True
#        except Exception,ex:
#            failure_reason=str(ex)
#            return False
def extractzip(fname,extractpath,createasfname=False):
    try:
        entryhasfile=False
        if createasfname==True:
            extractpath+= os.path.basename(fname)
        if not os.path.exists(extractpath):
            os.makedirs(extractpath)
        zipobj=zipfile.ZipFile(fname)
        fnames=zipobj.namelist()
        f=None
        for name in fnames:
            name=name.replace("/","\\")
            if name.find("\\")!=-1:
                if name.endswith("\\"):#empty directory
                   if not os.path.isdir(extractpath+"\\"+name):
                        os.makedirs(extractpath+"\\"+name)
                   entryhasfile=False
                else:
                     entryhasfile=True
                     if not os.path.isdir(extractpath+"\\"+name[:name.rfind("\\")]):
                         os.makedirs(extractpath+"\\"+name[:name.rfind("\\")])
            else:
                entryhasfile=True
            if entryhasfile:
                matter=zipobj.read(name.replace("\\","/"))
                f=open(extractpath+"\\"+name,"wb")
                f.write(matter)
                f.close()
        zipobj.close()
        return True
    except IOError,ie:
        failure_reason=str(ie)
        return False
    except Exception,ex:
        failure_reason=str(ex)
        return False

##def extractzip(fname,extractpath):
##    try:
##        if not os.path.exists(extractpath):
##            os.makedirs(extractpath)
##        zipobj=zipfile.ZipFile(fname)
##        fnames=zipobj.namelist()
##        f=None
##        for name in fnames:
##            matter=zipobj.read(name)
##            if len(matter)!=0:#we have a directory to create
##                name=name.replace("/","\\")
##                if name.find("\\")!=-1:
##                   os.makedirs(extractpath+"\\"+name[:name.rfind("\\")])
##                   f=open(extractpath+"\\"+name[name.rfind("\\")+1:],"wb")
##                else:
##                    f=open(extractpath+"\\"+name,"wb")
##                f.write(matter)
##                f.close()
##            else:
##                name=name.replace("/","\\")
##                if name.endswith("\\"):#no files in directory
##                    os.makedirs(extractpath+"\\"+name[:name.rfind("\\")])
##                else:
##                    os.makedirs(extractpath+"\\"+name[:name.rfind("\\")])
##                    f=open(extractpath+"\\"+name[name.rfind("\\")+1:],"wb")
##                    f.close()
##
##        zipobj.close()
##        return True
##    except IOError,ie:
##        return False
##    except Exception,ex:
##        return False
if __name__=='__main__':
    print modifyini(r"d:\payman\payman.ini", {'licenseserver':'localhost'})
    print failure_reason
    #print checkzip("C:\\Users\\adi\\Downloads\\request.900")
    #createzip("c:\\adi\\temp\\temp.ods",os.listdir("c:\\adi\\temp\\odstemp"),"c:\\adi\\temp\\odstemp")
##    #getwindowsserial()
##    parseini("C:\\Users\\adi\\python projs\\radha soami\\dist"+ "\\" + "logic.config",['InputBaseDir','OutputBaseDir','TallyHost','TallyPort'],"#")
##     print getwindowsinfo()
##    import time
##    sttime=time.time()
##    extractzip("c:\\adi\\temp\\gs.zip","c:\\adi\\temp\\gstemp")
##    endtime=time.time()
##    print "Total Time Take in (sec):-",endtime-sttime
##    print findmyini('c:/Users/adi/python projs/gaurdain/dist')
##    print parseini("sims1.ini",["serverip","serverport"],"#")
