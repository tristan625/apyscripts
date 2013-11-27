#Shree Ganeshayah Namah
import libxml2 as lb2
from apyscripts.utilityfuncs.utilityfuncs import extractzip,checkzip
from os.path import exists,isdir,isfile
from datetime import datetime,timedelta
from tempfile import gettempdir
import glob,types

class o2k7(object):
    _public_methods_=["readxlsx","getlasterror","readods","datanotimported","getlastprocessedrow","TDLCollection"]
    _reg_progid_ = "Logic.odimportutil"
    _reg_clsid_="{9c274cdb-cf6d-4abb-827f-265ff1efc382}"
    def __init__(self):
        self.__o2k7__lasterror=None
        self.__o2k7__filename=None
        self.__o2k7_temppath=gettempdir()
        self.__o2k7__xmlobj=None
        self.__o2k7__wrksheet_path="xl\\worksheets"
        self.__o2k7__sheetmatter=None
        self.__o2k7_sharedstringsfile="sharedStrings.xml"
        self.__o2k7__stylesfile="styles.xml"
        self.__o2k7_stringtable=dict()
        self.__o2k7__defaultdatestart=datetime(1900,1,1)
        self.__o2k7__defaulttimedeltaobj=None
        self.__o2k7__odsdatafile="content.xml"
        self.__o2k7__xmlobjdocelem=None
        self.__o2k7__namespaces=dict()
        self.__o2k7__sheetcellcount=0
        self.__o2k7__styledict=dict()
        self.__o2k7__baddata=list()
        self.__o2k7__lastrow__processed=0
        self.__o2k7__lastcell__processed=0
    def TDLCollection(self,fname,fnamexml):
        return "<A><B><C>12233344</C></B></A>"
    def __gatherbaddata(self,data):
        self.__o2k7__baddata.append(data)
    def __clearbaddata(self):
        self.__o2k7__baddata=[]
    def datanotimported(self):
        return self.__o2k7__baddata
    def getdocelem(self):
        return self.__o2k7__xmlobjdocelem
    def readods(self,fname,ignorestructure=False):
        self.__o2k7__filename=fname
        if exists(self.__o2k7__filename) and isfile(self.__o2k7__filename) and checkzip(self.__o2k7__filename):
            try:
                retval=self.__readodsdata(ignorestructure)
                if retval==False:
                    return False
                else:
                    return retval
            except Exception,ex:
                self.__o2k7__lasterror=str(ex)
                return False
        else:
            self.__o2k7__lasterror="Invalid File/Format"
            return False
    def __readodsdata(self,ignorestructure=False):
        table=[]
        record=[]
        self.__clearbaddata()
        if not self.__unpack():
            self.__o2k7__lasterror="Extraction Failure"
            return False
        f=open(self.__o2k7_temppath+"\\"+self.__o2k7__odsdatafile)
        matter=f.read(-1)
        f.close()
        rows=self.getvaluelist("//table:table-row",matter,True,populatens=True,autousens=True)
        for row in rows:
            cells=self.getvaluelist("table:table-cell",None,False,row,autousens=True)
            if self.__o2k7__sheetcellcount==0:
                self.__o2k7__sheetcellcount=len(cells)
            if len(cells)==0:
                continue
            for cell in cells:
                if cell.hasProp("number-columns-repeated")!=None:
                    columnstorepeat=cell.hasProp("number-columns-repeated").get_content()
                    for col in range(int(columnstorepeat)):
                        value_list=self.getvaluelist("text:p",None,False,cell,autousens=True)
                        if len(value_list)!=0:
                            record.append(value_list[0].get_content())
                        else:
                            record.append("")
                else:
                    value_list=self.getvaluelist("text:p",None,False,cell,autousens=True)
                    if len(value_list)!=0:
                        record.append(value_list[0].get_content())
                    else:
                        record.append('')
            if not ignorestructure:
                if len(record)!=0 and len(record)==self.__o2k7__sheetcellcount:
                    table.append(record)
                elif len(record)==0:
                    continue
                else:
                    ncellsmissing=self.__o2k7__sheetcellcount-len(record)
                    if ncellsmissing < 0:
                        ncellsmissing=0
                        record=record[:self.__o2k7__sheetcellcount]
                        table.append(record)
                    if ncellsmissing > 0:
                        for cell in range(ncellsmissing):
                            record.append("")
                        table.append(record)
                    else:
                        self.__gatherbaddata([len(record),record,self.__o2k7__sheetcellcount,ncellsmissing])
            else:
                table.append(record)
            self.__o2k7__lastrow__processed=self.__o2k7__lastrow__processed+1
            record=[]
        return table
    def readxlsx(self,fname):
        self.__o2k7__filename=fname
        if exists(self.__o2k7__filename) and isfile(self.__o2k7__filename) and checkzip(self.__o2k7__filename):
            try:
                retval=self.__readdata()
                if retval==False:
                    return False
                else:
                    return retval
            except Exception,ex:
                self.__o2k7__lasterror=str(ex)
                return False
        else:
            self.__o2k7__lasterror="Invalid File/Format"
            return False
    def __readstyles(self):
        try:
            f=open(self.__o2k7_temppath+"xl"+"\\"+self.__o2k7__stylesfile)
            matter=f.read(-1)
            f.close()
        except IOError,ie:
            self.__o2k7__lasterror=str(ie)
            return False
        matter=matter.replace("xmlns=","")
        matter=matter.replace('"http://schemas.openxmlformats.org/spreadsheetml/2006/main"',"")
        styles=self.getvaluelist("/styleSheet/cellXfs/xf",matter,True)
        for i in range(len(styles)):
            self.__o2k7__styledict[i]=styles[i].hasProp("numFmtId").get_content()
        return True

    def __readsharedstrings(self):
        try:
            f=open(self.__o2k7_temppath+"xl"+"\\"+self.__o2k7_sharedstringsfile)
            matter=f.read(-1)
            f.close()
        except IOError,ie:
            self.__o2k7__lasterror=str(ie)
            return False
        matter=matter.replace("xmlns=","")
        matter=matter.replace('"http://schemas.openxmlformats.org/spreadsheetml/2006/main"',"")
        string_list=self.getvaluelist("//t",matter,True)
        for i in range(len(string_list)):
            self.__o2k7_stringtable[i]=string_list[i].get_content()
        return True
    def calclastusedcell(self,lcell):
      return self.__calclastusedcell(lcell)
    def __calclastusedcell(self,lcell):
        clcell=[]
        fpart=""
        for c in range(len(lcell)):
            if ord(lcell[c]) in range(65, 91):
                clcell.append(lcell[c])
                continue
            else:
                if clcell[c-1]not in ["Z","z"]:
                    clcell[c-1]=chr(ord(lcell[c-1])+1)
                else:
                    if len(clcell)==1:
                        fpart="A" * (len(clcell)+1)
                        fpart+=lcell[len(clcell):]
                        return fpart
                    else:
                        for elem in range(len(clcell)):
                            if clcell[elem]in ["Z","z"]:
                                clcell[elem]="A"
                            else:
                                clcell[elem]=chr(ord(clcell[elem])+1)
                fpart="".join(clcell)
                fpart+=lcell[len(clcell):]
                return fpart
    def __readdata(self,sheetno=1):
        table=[]
        record=[]
        alphalist=map(chr, range(65, 91))
        last_used_cell=None
        self.__clearbaddata()
        if not self.__unpack():
            self.__o2k7__lasterror="Extraction Failure"
            return False
        if not self.__readstyles():
            return False
        if not self.__readsharedstrings():
            return False
        sheetname=self.__o2k7_temppath+self.__o2k7__wrksheet_path+"\\sheet%s.xml" % sheetno
        try:
            f=open(sheetname,"r")
            self.__o2k7__sheetmatter=f.read(-1)
            f.close()
        except IOError,ie:
             self.__o2k7__lasterror=str(ie)
             return False
        ##Get rid of the xml namespaces so that we can carry out xpath calls successfully
        self.__o2k7__sheetmatter=self.__o2k7__sheetmatter[self.__o2k7__sheetmatter.find("<sheetData>"):self.__o2k7__sheetmatter.rfind("</sheetData>")+len("</sheetData>")]
        ## Gather all rows from the excel sheet
        rows=self.getvaluelist("//row",self.__o2k7__sheetmatter,True)
        if len(rows)==0:
            self.__o2k7__lasterror="No Data Available"
            return False
        ## Iterate over the rows retreived to gather cells and their values
        for row in rows:
            cells=self.getvaluelist("c",None,False,row)
            if self.__o2k7__sheetcellcount==0:
                self.__o2k7__sheetcellcount=len(cells)
                #print len(cells)
            for cell in cells:
                if last_used_cell!=None:
##                      print self.__calclastusedcell(last_used_cell),cell.hasProp("r").get_content()
                        ##if chr(ord(last_used_cell[0])+1)!=cell.hasProp("r").get_content()[0]:
                      if self.__calclastusedcell(last_used_cell)!=cell.hasProp("r").get_content():
                          while self.__calclastusedcell(last_used_cell)!=cell.hasProp("r").get_content():
                                record.append("") # excel skipped empty cell
                                last_used_cell=self.__calclastusedcell(last_used_cell)
                value_list=self.getvaluelist("v",None,False,cell)
                if len(value_list)!=0:
                    type_attrib=cell.hasProp("t")
                    if type_attrib!=None:
                        if type_attrib.get_content()=='s':
                            record.append(self.__o2k7_stringtable[int(value_list[0].get_content())])
                        if type_attrib.get_content()=='b':
                            if int(value_list[0].get_content())==1:
                                record.append(True)
                            else:
                                record.append(False)
                        if type_attrib.get_content()=='n':
                            record.append(value_list[0].get_content())
                    elif cell.hasProp("s")!=None:
                         style_val= cell.hasProp("s").get_content()
                         if self.__o2k7__styledict[int(style_val)]=='14':
                             self.__o2k7__defaulttimedeltaobj=timedelta(days=int(value_list[0].get_content())-2)
                             ext_date=self.__o2k7__defaultdatestart+self.__o2k7__defaulttimedeltaobj
                             record.append(ext_date.strftime("%d-%m-%Y"))
                             del ext_date
                         else:
                             record.append(value_list[0].get_content())
                    else:
                        record.append(value_list[0].get_content())
                else:
                    record.append('')
                last_used_cell=cell.hasProp("r").get_content()
            if len(record)!=0 and len(record)==self.__o2k7__sheetcellcount:
                table.append(record)
            elif len(record)==0:
              continue
            else:
                ncellsmissing=self.__o2k7__sheetcellcount-len(record)
                if ncellsmissing < 0:
                    ncellsmissing=0
                    record=record[:self.__o2k7__sheetcellcount]
                    table.append(record)
                if ncellsmissing > 0:
                    for cell in range(ncellsmissing):
                        record.append("")
                    table.append(record)
                else:
                    self.__gatherbaddata([len(record),record,self.__o2k7__sheetcellcount,ncellsmissing])
            self.__o2k7__lastrow__processed=self.__o2k7__lastrow__processed+1
            record=[]
            last_used_cell=None
        return table
    def getlastprocessedrow(self):
        return self.__o2k7__lastrow__processed
    def __populatenamespaces(self,prefix,uri):
        self.__o2k7__namespaces[prefix]=uri
    def getvaluelist(self,path,matter,doparse=False,cnode=None,populatens=True,autousens=False,namespace=None):
        try:
            if doparse==False and self.__o2k7__xmlobj==None:
                self.__o2k7__xmlobj=lb2.parseMemory(matter,len(matter))
            elif doparse==True:
                if self.__o2k7__xmlobj!=None:
                    self.__o2k7__xmlobj.freeDoc()
                self.__o2k7__xmlobj=lb2.parseMemory(matter,len(matter))
                self.__o2k7__xmlobjdocelem=self.__o2k7__xmlobj.getRootElement()
                if populatens ==True and self.__o2k7__xmlobjdocelem.nsDefs()!=None:
                    for ns in self.__o2k7__xmlobjdocelem.nsDefs():
                        self.__populatenamespaces(ns.name,ns.get_content())
            if cnode!=None and populatens ==True and cnode.nsDefs()!=None:
                 for ns in cnode.nsDefs():
                        self.__populatenamespaces(ns.name,ns.get_content())
            xpcontext=self.__o2k7__xmlobj.xpathNewContext()
            if autousens==True or namespace!=None:
                if autousens==True:
                    for ns in self.__o2k7__namespaces:
                         xpcontext.xpathRegisterNs(ns,self.__o2k7__namespaces[ns])
            if cnode==None:
                xpcontext.setContextNode(self.__o2k7__xmlobj)
            else:
                xpcontext.setContextNode(cnode)
            result=xpcontext.xpathEval(path)
            xpcontext.xpathFreeContext()
            return result
        except lb2.parserError,pe:
            self.__o2k7__lasterror=str(pe)
            return False
        except lb2.libxmlError,lx:
            self.__o2k7__lasterror=str(lx)
            return False
        except Exception,ex:
            self.__o2k7__lasterror=str(ex)
            return False
    def __unpack(self):
        return extractzip(self.__o2k7__filename,self.__o2k7_temppath)
    def getlasterror(self):
        if self.__o2k7__lasterror!=None:
            return self.__o2k7__lasterror
        else:
            return ""

if __name__=='__main__':
    xlsxobj=o2k7()
    import os,types
#    retval=xlsxobj.readods("C:\\Users\\adi\\Downloads\\excelfile.ods")
    retval=xlsxobj.readxlsx(r"C:\Users\adi\Downloads\Bookss.xlsx")
    if type(retval)==types.BooleanType:
        print xlsxobj.getlasterror()
    else:
        print len(retval[2])
        print retval[2]
        #print retval
    ##xlsxobj.calclastusedcell("Z1")
##    retval=xlsxobj.readxlsx("C:\\Users\\adi\\python projs\\office2007\\dist\\book2.xlsx")
##    for g in retval:
##        if len(g) != 63:
##            print g
##    #print retval,"\n"
##    print len(retval)
##    print retval[20]
##    print retval[21]
##    print xlsxobj.datanotimported()
##
