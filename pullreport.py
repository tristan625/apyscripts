from apyscripts.remoteio import remoteio
from apyscripts.fragment import TallyFragment
#from fragmenterp import TallyErpFragment
class Pull(object):
    __author__="adi"
    __date__ ="$Feb 27, 2009 11:42:00 AM$"
    def __init__(self):
        self.__pull__httpobj=remoteio()
        self.__pull__fragobj=TallyFragment()
#        self.__pull__erpfragobj=TallyErpFragment()
        self.__pull__srcport=9000
        self.__pull__srcip="localhost"
        self.__pull__cname=None
        self.__pull__reportdict=dict()
        self.__pull__last__failure__reason=""
    def setstatics(self,srcport,srcip,cname):
        self.__pull__srcport=srcport
        self.__pull__srcip=srcip
        self.__pull__cname=cname
    def definereport(self,repname,*stvars):
        reportvars=[]
        for var in stvars:
            reportvars.append(var)
        self.__pull__reportdict[repname]=reportvars
    def pullreportforerp(self,isource,modulename,*stvars):
        stdict=None
        if not self.__pull__reportdict.has_key(modulename):
            return False
        if len(stvars)!=len(self.__pull__reportdict[modulename]):
            return False
        if len(self.__pull__reportdict[modulename])!=0:
            rvars=self.__pull__reportdict[modulename]
            stdict=dict()
            for stvar in range(len(rvars)):
                stdict[rvars[stvar]]=stvars[stvar]
        if stdict!=None:
            reqmatter=self.__pull__erpfragobj.preparefragment(isource,modulename,stdict)
        else:
            reqmatter=self.__pull__erpfragobj.preparefragment(isource,modulename)
        self.__pull__httpobj.setconnectionparams(self.__pull__srcip, self.__pull__srcport)
        retmatter=self.__pull__httpobj.getdata(reqmatter)
        if retmatter != None:
                return retmatter
        else:
            self.__pull__last__failure__reason=self.__pull__httpobj.getlasterror()
            return False
    def pullreport(self,repname,*stvars):
        if not self.__pull__reportdict.has_key(repname):
            return False
        if len(stvars)!=len(self.__pull__reportdict[repname]):
            return False
        if len(self.__pull__reportdict[repname])!=0:
            rvars=self.__pull__reportdict[repname]
            for var in range(len(rvars)):
                self.__pull__fragobj.addstaticvar(rvars[var]+":"+stvars[var])
        reqmatter=self.__pull__fragobj.preparefragment(1, repname, self.__pull__cname)
        self.__pull__httpobj.setconnectionparams(self.__pull__srcip, self.__pull__srcport)
        retmatter=self.__pull__httpobj.getdata(reqmatter)
        ##retmatter=self.__pull__httpobj.getdataviarequestobj(reqmatter)
        if retmatter != None:
            return retmatter
        else:
            self.__pull__last__failure__reason=self.__pull__httpobj.getlasterror()
            return False
    def getpreparedmatter(self,repname,pushmatter,cname=None):
        if cname is None:
            return self.__pull__fragobj.preparefragment(2, repname, self.__pull__cname,pushmatter)
        else:
            return self.__pull__fragobj.preparefragment(2, repname, cname,pushmatter)
    def pushreport(self,repname,pushmatter):
        reqmatter=self.__pull__fragobj.preparefragment(2, repname, self.__pull__cname,pushmatter)
        self.__pull__httpobj.setconnectionparams(self.__pull__srcip, self.__pull__srcport)
        ##retmatter=self.__pull__httpobj.getdata(reqmatter)
        retmatter=self.__pull__httpobj.getdataviarequestobj(reqmatter)
        if retmatter != None:
            return retmatter
        else:
            self.__pull__last__failure__reason=self.__pull__httpobj.getlasterror()
            return False
    def pushdataasis(self,pushmatter):
        ##reqmatter=self.__pull__fragobj.preparefragment(2, repname, self.__pull__cname,pushmatter)
        self.__pull__httpobj.setconnectionparams(self.__pull__srcip, self.__pull__srcport)
        ##retmatter=self.__pull__httpobj.getdata(pushmatter)
        retmatter=self.__pull__httpobj.getdataviarequestobj(pushmatter)
        if retmatter != None:
            return retmatter
        else:
            self.__pull__last__failure__reason=self.__pull__httpobj.getlasterror()
            return False
    def getlasterror(self):
        return self.__pull__last__failure__reason

if __name__ == "__main__":
    dd=Pull()
    #print dd.__author__
    dd.setstatics(9000,"localhost", "Kapoor Enterprises")
    dd.definereport("MDFDayBookAlterID","MDFSVFromDate","MDFSVToDate","MDFVOUCHERTYPENAME")
    print dd.pullreport("MDFDayBookAlterID","01-01-2010","01-01-2012","Receipt")
    ##print dd.pullreport("MDFSyncFilterEXPListofAccounts","01-04-2008","01-06-2008","Voucher Types")