#Shree Ganeshayah Namah
from fragment import TallyFragment
import win32com.client
import pythoncom
from win32con import *

class TallyFragmentCustom(TallyFragment):
    """This is class and other classes on the same line are supposed
    to provide custom operations on Tally Data Fragments"""
    def __init__(self):
        self.__payload=''
        self.__failure_reason=''
        self.__msxml__xslt__obj=None
        self.__msxml__xslt__doc=None
        pythoncom.CoInitialize ()
        self.__msxml_obj=win32com.client.Dispatch(r"msxml2.DOMDocument.6.0")
        self.__msxml_obj.setProperty("SelectionLanguage", "XPath")
        self.__msxml_obj.setProperty("SelectionNamespaces", "xmlns:UDF='TallyUDF'")
        self.__msxml_obj.async=False
        self.__msxml_obj.preserveWhiteSpace=True
#        self.__stvarlist=[]
        TallyFragment.__init__(self)
#        TallyFragment.__init__(self)
    def transformfrag(self,stylesheet,matter):
        if self.load(matter)==True:
            self.__msxml__xslt__obj=win32com.client.Dispatch(r"Msxml2.XSLTemplate.4.0")
            self.__msxml__xslt__doc=win32com.client.Dispatch(r"Msxml2.FreeThreadedDOMDocument.4.0")
            self.__msxml__xslt__doc.async=False
            self.__msxml__xslt__doc.loadXML(stylesheet)
            self.__msxml__xslt__obj.stylesheet=self.__msxml__xslt__doc
            processor=self.__msxml__xslt__obj.createProcessor()
            processor.input=self.__msxml_obj
            processor.transform()
            return processor.output
        else:
            return None
    def addnode(self,nodename,nodetype):
        raise NotImplementedError
    def addelement(self,elemname):
        return self.__msxml_obj.createElement(elemname)
    def cstop(self,matter):
        """ This function will convert a Tally Sale Voucher Fragment
        To a Purchase Voucher Fragment"""
        if self.__load(matter)==True:
            nodelist=self.__filter("//VOUCHER[@VCHTYPE='Stock Transfer (Outward)']")
            r_matter=''
            for node in nodelist:
                self.__changeattribute(node)
                r_matter+=self.__wrap(node.xml)
            return r_matter
        else:
            return ""

    def load(self,matter):
        """Build the dom tree for our xml fragment"""
        try:
            self.__msxml_obj.loadXML(matter)
            if self.__msxml_obj.parseError.errorCode==0:
                return True
            else:
                self.__failure_reason=self.__msxml_obj.parseError.reason + "\n" + str(self.__msxml_obj.parseError.line) + "\n" + str(self.__msxml_obj.parseError.linepos) + "\n" + str(self.__msxml_obj.parseError.srcText)
                return False
        except Exception,e:
            if hasattr(e,'reason'):
                self.__failure_reason=e.reason
                return False
            elif hasattr(e,'code'):
                self.__failure_reason=e.code
                return False
            else:
                self.__failure_reason=str(e)
                return False
    def getrootelem(self):
        return self.__msxml_obj.documentElement
    def filter(self,condition,cnode=None):
        """This function returns a nodelist after filtering the
        fragment for the specified condition,supply a valid
        xml Node element to in the context of that Node"""
        if cnode!=None:
            nodelist=cnode.selectNodes(condition)
        else:
            nodelist=self.__msxml_obj.selectNodes(condition)
        return nodelist

    def filtersingle(self,condition,cnode=None):
        """This function returns a nodelist after filtering the
        fragment for the specified condition"""
        if cnode!=None:
            node=cnode.selectSingleNode(condition)
        else:
            node=self.__msxml_obj.selectSingleNode(condition)
        return node

    def __changeattribute(self,domnode):
        """ function to make necessary replacements in the fragments"""
        domnode.attributes.item(1).text="Stock Transfer (Inward)" ## Replacing the VCHTYPE Attribute value
        if domnode.hasChildNodes() == True:
                for child in domnode.childNodes:
                    if child.nodeType==1 and child.nodeName=="VOUCHERTYPENAME":
                        child.text="Stock Transfer (Inward)"
                    if child.nodeType==1 and child.nodeName=="ISINVOICE":
                        child.text="NO"
                    if child.nodeType==1 and child.nodeName=="ALLINVENTORYENTRIES.LIST":
                        for schild in child.childNodes:
                            if schild.nodeType==1 and schild.nodeName=="ACCOUNTINGALLOCATIONS.LIST":
                                for invchild in schild.childNodes:
                                    if invchild.nodeType==1 and invchild.nodeName=="LEDGERNAME" and invchild.text=="Stock Transfer (Outward)":
                                        invchild.text="Stock Transfer (Inward)"

    def wrap(self,matter):
        """This function wraps the matter arg in Tallymessage tags using the
            import midrif function of the base class"""
        matter=TallyFragment.getImportMidRif(self,matter)
        return matter

    def isexportsuccessfull(self,matter):
        if self.load(matter)==True:
           if self.filtersingle("//LINEERROR")!=None or self.filtersingle("//LINEERROR[@ID]")!=None:
               return False
           else:
                return True
        else:
            return False

    def isimportsuccessfull(self,matter):
        if self.load(matter)==True:
            if self.filtersingle("//LINEERROR")==None or self.filtersingle("//LINEERROR[@ID]")==None:
                if (int(self.filtersingle("//CREATED").text)!=0 or int(self.filtersingle("//ALTERED").text)!=0) and int(self.filtersingle("//ERRORS").text)==0:
                    return True
                else:
                    return False
            else:
                return False
    def getlasterror(self):
        return self.__failure_reason