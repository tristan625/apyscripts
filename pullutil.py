#Shree Ganeshayah Namah

from pullreport import Pull
import libxml2 as lb2
class Utilitypull(Pull):
    """ utility class that contains predefined functions for pulling common
        TDL based reports from tally
    """
    rootelem=None
    def __init__(self):
        Pull.__init__(self)
        self.__utilpull__last__failure__reason=None
        self.rootelem=None
        self.xpcontext=None
        self.__voucher__template = """<VOUCHER  VCHTYPE="Sales Order" ACTION="Create" OBJVIEW="Invoice Voucher View">
        <BASICBUYERADDRESS.LIST TYPE="String">
        <BASICBUYERADDRESS/>
        </BASICBUYERADDRESS.LIST>
        <DATE/>
        <PARTYNAME/>
        <VOUCHERTYPENAME/>
        <VOUCHERNUMBER/>
        <REFERENCE/>
        <PARTYLEDGERNAME/>
        <BASICBASEPARTYNAME/>
        <BASICSHIPPEDBY/>
        <BASICBUYERNAME/>
        <BASICFINALDESTINATION/>
        <EFFECTIVEDATE/>
        <NARRATION/>
        <LEDGERENTRIES.LIST>
        <LEDGERNAME/>
        <ISDEEMEDPOSITIVE/>
        <ISPARTYLEDGER/>
        <AMOUNT/>
        </LEDGERENTRIES.LIST>
        </VOUCHER>
        """
        
        self.__ledger__template = """
        <LEDGER NAME="" RESERVEDNAME="">
        <PARENT/>
      <ISBILLWISEON>No</ISBILLWISEON>
      <LANGUAGENAME.LIST>
       <NAME.LIST TYPE="String">
        <NAME/>
       </NAME.LIST>
       <LANGUAGEID> 1033</LANGUAGEID>
      </LANGUAGENAME.LIST>
      <ADDRESS.LIST TYPE="String">
       <ADDRESS/>
      </ADDRESS.LIST>
      <MAILINGNAME.LIST TYPE="String">
       <MAILINGNAME/>
      </MAILINGNAME.LIST>
      <STATENAME/>
      <PINCODE/>
      <INCOMETAXNUMBER/>
      <SALESTAXNUMBER/>
      <INTERSTATESTNUMBER/>
      <EMAIL/>
      <LEDGERPHONE/>
      <LEDGERFAX/>
      <LEDGERCONTACT/>
      <LEDGERMOBILE/>
      <AFFECTSSTOCK>No</AFFECTSSTOCK>
      <OPENINGBALANCE/>
      <BILLCREDITPERIOD/>
     </LEDGER>
     """
        self.__item__template="""<TALLYMESSAGE><STOCKITEM NAME='' RESERVEDNAME="">
      <PARENT/>
      <CATEGORY/>
      <TAXCLASSIFICATIONNAME/>
      <COSTINGMETHOD>Avg. Cost</COSTINGMETHOD>
      <VALUATIONMETHOD>Avg. Price</VALUATIONMETHOD>
      <BASEUNITS/>
      <ADDITIONALUNITS/>
      <DESCRIPTION/>
      <NARRATION/>
      <EXCISEITEMCLASSIFICATION>Default</EXCISEITEMCLASSIFICATION>
      <BASICTARIFFTYPE/>
      <TCSCATEGORY/>
      <ISCOSTCENTRESON>No</ISCOSTCENTRESON>
      <ISBATCHWISEON>No</ISBATCHWISEON>
      <ISPERISHABLEON>No</ISPERISHABLEON>
      <ISENTRYTAXAPPLICABLE>No</ISENTRYTAXAPPLICABLE>
      <IGNOREPHYSICALDIFFERENCE>No</IGNOREPHYSICALDIFFERENCE>
      <IGNORENEGATIVESTOCK>No</IGNORENEGATIVESTOCK>
      <TREATSALESASMANUFACTURED>No</TREATSALESASMANUFACTURED>
      <TREATPURCHASESASCONSUMED>No</TREATPURCHASESASCONSUMED>
      <TREATREJECTSASSCRAP>No</TREATREJECTSASSCRAP>
      <HASMFGDATE>No</HASMFGDATE>
      <ALLOWUSEOFEXPIREDITEMS>No</ALLOWUSEOFEXPIREDITEMS>
      <IGNOREBATCHES>No</IGNOREBATCHES>
      <IGNOREGODOWNS>No</IGNOREGODOWNS>
      <EXCLUDEJRNLFORVALUATION>No</EXCLUDEJRNLFORVALUATION>
      <ISMRPINCLOFTAX>No</ISMRPINCLOFTAX>
      <ISADDLTAXEXEMPT>No</ISADDLTAXEXEMPT>
      <ISSUPPLEMENTRYDUTYON>No</ISSUPPLEMENTRYDUTYON>
      <REORDERASHIGHER>No</REORDERASHIGHER>
      <MINORDERASHIGHER>No</MINORDERASHIGHER>
      <DENOMINATOR> 1</DENOMINATOR>
      <BASICRATEOFEXCISE/>
      <RATEOFVAT/>
      <OPENINGBALANCE/>
      <OPENINGVALUE/>
      <OPENINGRATE/>
      <MAILINGNAME.LIST TYPE="String">
           <MAILINGNAME/>
      </MAILINGNAME.LIST>
      <LANGUAGENAME.LIST>
          <NAME.LIST TYPE="String">
             <NAME/>
          </NAME.LIST>
          <LANGUAGEID> 1033</LANGUAGEID>
      </LANGUAGENAME.LIST>
      <STANDARDCOSTLIST.LIST>
       <DATE/>
       <RATE/>
      </STANDARDCOSTLIST.LIST>
      <STANDARDPRICELIST.LIST>
       <DATE/>
       <RATE/>
      </STANDARDPRICELIST.LIST>
      </STOCKITEM>
      </TALLYMESSAGE>"""
##      <!-- Batch Allocations are Applicable Only If We Have Some Opening Quantity-->
##      <BATCHALLOCATIONS.LIST>
##       <GODOWNNAME>Main Location</GODOWNNAME>
##       <BATCHNAME>Primary Batch</BATCHNAME>
##       <OPENINGBALANCE/>
##       <OPENINGVALUE/>
##       <OPENINGRATE/>
##      </BATCHALLOCATIONS.LIST>

    def getledgertemplate(self):
        return self.__ledger__template
    
    def getitemtemplate(self):
        return self.__item__template
    
    def getvouchertemplate(self):
        return self.__voucher__template
    
    def sanitizeforxml(self,content):
        return self.rootelem.encodeSpecialChars(content)

    def getitemtemplateasobject(self):
        nodelist=self.getvaluelist("//STOCKITEM",self.__item__template,True)
        return nodelist[0]

    def getcompanies(self):
        self.definereport("List Of Companies")
        retmatter=self.pullreport("List Of Companies")
        if retmatter not in [False,None] and self.isexportsuccessfull(retmatter):
            vlist=self.getvaluelist("//COMPANYNAME",retmatter,True)
            if vlist not in [None,False]:
                return [elem.get_content() for elem in vlist]
        else:
            self.__utilpull__last__failure__reason=Pull.getlasterror(self)
            return False

    def getaddons(self):
        self.definereport("MDFAddons")
        retmatter=self.pullreport("MDFAddons")
        if retmatter not in [False,None]:
            vlist=self.getvaluelist("//MDFADDONNAME",retmatter,True)
            if vlist not in [False,None]:
                return [elem.get_content() for elem in vlist]
        else:
            self.__utilpull__last__failure__reason=Pull.getlasterror(self)
            return False

    def getvouchertypes(self,repname="List Of Accounts"):
        self.definereport(repname,"ACCOUNTTYPE")
        retmatter=self.pullreport(repname,"VOUCHERTYPES")
        if retmatter not in [False,None]:
            vlist=self.getvaluelist("//VOUCHERTYPE",retmatter,True)
            if vlist not in [False,None]:
                return [elem.get_properties().get_content() for elem in vlist ]
        else:
            self.__utilpull__last__failure__reason=Pull.getlasterror(self)
            return False

    def getledgers(self):
        self.definereport("List Of Accounts","ACCOUNTTYPE")
        retmatter=self.pullreport("List Of Accounts","LEDGERS")
        if retmatter not in [False,None]:
##            self.logmatter(retmatter)
            return [elem.get_properties().get_content() for elem in self.getvaluelist("//LEDGER",retmatter)]
        else:
            self.__utilpull__last__failure__reason=Pull.getlasterror(self)
            return False
        
    def getvaluelist(self,path,matter,doparse=False,cnode=None,usehtml = False):
        try:
            if doparse==False and self.rootelem==None:
                if usehtml:
                    self.rootelem=lb2.htmlParseDoc(matter,"utf-8")
                else:    
                    self.rootelem=lb2.parseMemory(matter,len(matter))
            elif doparse==True:
                if self.rootelem!=None:
                    self.rootelem.freeDoc()
                    self.xpcontext.xpathFreeContext()
                self.rootelem=lb2.parseMemory(matter,len(matter))
            self.xpcontext=self.rootelem.xpathNewContext()
            if cnode==None:
                self.xpcontext.setContextNode(self.rootelem)
            else:
                self.xpcontext.setContextNode(cnode)
            result=self.xpcontext.xpathEval(path)
            return result
        except lb2.parserError,pe:
            self.__utilpull__last__failure__reason=str(pe)
            return False
        except lb2.libxmlError,lx:
            self.__utilpull__last__failure__reason=str(lx)
            return False
        except Exception,ex:
            self.__utilpull__last__failure__reason=str(ex)
            return False

    def getrootelem(self):
        return self.rootelem

    def logmatter(self,matter):
        f=open("logmatter","wb")
        f.write(matter)
        f.close()

    def isexportsuccessfull(self,matter):
        retval=self.getvaluelist("//LINEERROR",matter,True)
        if retval !=False:
            if len(retval)==0 :
                return True
            else:
                return False
        else:
            return False

    def isimportsuccessfull(self,matter):
        retval=self.getvaluelist("//LINEERROR",matter,True)
        ferrors=self.getvaluelist("//ERRORS",matter)
        altc=self.getvaluelist("//ALTERED",matter)
        createc=self.getvaluelist("//CREATED",matter)
        cmbc=self.getvaluelist("//COMBINED",matter)
        inorc=self.getvaluelist("//IGNORED",matter)
        if retval!=False or ferrors !=False or altc !=False or createc !=False or cmbc !=False or inorc!=False:
            try:
                if len(retval)==0 and (len(ferrors)==0 or int(ferrors[0].get_content())==0) and (altc!=0 or createc!=0 or comb!=0 or inorc!=0):
                    return True
                else:
                    return False
            except ValueError,ex:
                self.__utilpull__last__failure__reason=str(ex)
                return True
            except Exception,ex:
                self.__utilpull__last__failure__reason=str(ex)
                return False

        else:
            return False

    def getlasterror(self):
        if self.__utilpull__last__failure__reason==None:
            ## we have an error encountered in the parent module
            self.__utilpull__last__failure__reason=Pull.getlasterror(self)
        return self.__utilpull__last__failure__reason
    
if __name__=='__main__':
    hh=Utilitypull()
##    import time
##    st=time.time()
    import socket
##
    hh.setstatics(9000,"172.16.10.130",None)
    ##hh.definereport("MDFLEntryReport")
    hh.definereport("List Of Companies")
    print hh.pullreport("List Of Companies")
    print hh.getlasterror()
####    print hh.getvouchertypes()
##    print hh.getcompanies()
####    print hh.getledgers()
##    ent=time.time()
##    print "Total Time",ent-st
