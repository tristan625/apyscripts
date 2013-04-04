#Shree Ganeshayah Namah

class TallyFragment:

    """Class to format request data to retrieve data from Tally running on a
    specified host and port"""

    def __init__(self):
        self.__optype=''
        self.__report=''
        self.__cname=''
        self.__stvarlist=[]

    def __getExportHeader(self):
        """
           Prepares the header portion for a export
           request.
        """
        matter="""<ENVELOPE><HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER><BODY><EXPORTDATA>"""
        return matter

    def __getImportHeader(self):
        matter="<ENVELOPE>\n<HEADER>\n<TALLYREQUEST>Import Data</TALLYREQUEST>\n</HEADER>\n<BODY>\n<IMPORTDATA>\n"
        matter+="<REQUESTDESC>\n<REPORTNAME>"+ self.__report +"</REPORTNAME>\n<STATICVARIABLES>\n<SVCURRENTCOMPANY>"+ self.__cname +"</SVCURRENTCOMPANY>\n"
        matter+="<SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>\n</STATICVARIABLES>\n"
        matter+="</REQUESTDESC>\n<REQUESTDATA>\n"
        return matter

    def __getExportFooter(self):
        matter='</EXPORTDATA></BODY></ENVELOPE>'
        return matter

    def __getImportFooter(self):
        matter='</REQUESTDATA></IMPORTDATA></BODY></ENVELOPE>'
        return matter

    def __getExportMidRif(self):
        matter='<REQUESTDESC><REPORTNAME>'+ self.__report +'</REPORTNAME><STATICVARIABLES>'
        if len(self.__cname)!=0:
            matter+='<SVCURRENTCOMPANY>'+ self.__cname +'</SVCURRENTCOMPANY>'
        matter+='<SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>'
        if len(self.__stvarlist)<>0:
            for stvar in self.__stvarlist:
                delimpos=stvar.rfind(":")
                matter+="<"+ stvar[:delimpos] + ">" + stvar[delimpos+1:] + "</" + stvar[:delimpos] + ">"
        matter+='</STATICVARIABLES>'
        matter+='</REQUESTDESC><REQUESTDATA><TALLYMESSAGE></TALLYMESSAGE></REQUESTDATA>'
        return matter

    def __getImportMidRif(self,xmatter):
        matter="<TALLYMESSAGE>\n"
        matter+=xmatter
        matter+="</TALLYMESSAGE>\n"
        return matter

    def getImportMidRif(self,matter):
        #MessageBox(NULL,matter,"LOTUS",MB_OK)
        return self.__getImportMidRif(matter)

    def preparefragment(self,optype,reportname,cname,fragmatter=''):
        self.__optype=optype
        self.__report=reportname
        self.__cname=cname
        if self.__cname==None:
            self.__cname=""
        if self.__optype==1: #we are supposed to export data
            matter=self.__getExportHeader() + self.__getExportMidRif() + self.__getExportFooter()
        else:
            matter=self.__getImportHeader() + self.__getImportMidRif(fragmatter) + self.__getImportFooter()
        return matter
    def addstaticvar(self,var):
        self.__stvarlist.append(var)