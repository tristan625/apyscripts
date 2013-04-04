#Shree Ganeshayah Namah

from parsetdl import Tdlparser,Tdlcontenthandler
class TallyErpFragment(Tdlparser):
    def __init__(self):
        self.__terpfrag__chandler=Tdlcontenthandler()
        self.__terpfrag__repname=None
        self.__terpfrag__stvars=None
        Tdlparser.__init__(self)
    def addstaticvar(self,varlist):
        self.__terpfrag__stvars=varlist
    def __fragheader(self):
        return """<ENVELOPE><HEADER><VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Data</TYPE><ID>%s</ID></HEADER>
        <BODY><DESC>
        """ % self.__terpfrag__repname
    def __fragmidrif(self):
        matter=""
        if self.__terpfrag__stvars==None:
            self.__terpfrag__stvars=dict()
        self.__terpfrag__stvars["SVEXPORTFORMAT"]="$$SysName:XML"
        if self.__terpfrag__stvars!=None:
            matter+="<STATICVARIABLES>"
            for var in self.__terpfrag__stvars:
                matter+="<%s>%s</%s>" % (var,self.__terpfrag__stvars[var],var)
            matter+="</STATICVARIABLES>"
        matter+="<TDL>%s</TDL>" % self.__getfragment()
        return matter
    def __fragfooter(self):
        return """</DESC></BODY></ENVELOPE>
         """
    def preparefragment(self,isource,modulename,stvars=None):
        if stvars!=None:
            self.__terpfrag__stvars=stvars
        self.setinputsource(isource)
        self.setcontenthandler(self.__terpfrag__chandler)
        self.__terpfrag__repname=modulename
        matter=self.__fragheader() +  self.__fragmidrif() + self.__fragfooter()
        f=open("erpsamp.xml","wb")
        f.write(matter)
        f.close()
        return matter
    def __getfragment(self):
        self.parse()
        return Tdlparser.getfragment(self)

if __name__=='__main__':
    tfobj=TallyErpFragment()
    print tfobj.preparefragment("c:\\adi\\daybook.enc","MDFSyncFilterEXPList of Accounts")