#Shree Ganeshayah Namah
import types
class SimpleHtmlTableClass(object):
    """ A utility class to display a dataset in the
     form of a table
    """
    def __init__(self):
        self.shtc__payload=None
        self.shtc__headers=None
        self.shtc__matter=None
        self.shtc__processing__headers=False
        self.shtc__tblname=None
        self.shtc__paginate__buttons =1
    def setpagination(self,paginate = False, useimages=True):
        self.shtc__drawpaginated = paginate
        self.shtc__paginate__buttons = useimages
    def setheaders(self,headers):
        self.shtc__headers=headers
    def setpayload(self,payload):
        self.shtc__payload=payload
    def settablestyle(self,classname):
        self.shtc__tblstyle=classname
    def __drawrow(self,row,id):
        retval=""
        retval="<tr id='%sR%s'>" % (self.shtc__tblname,id)
        for cell in range(len(row)):
            cellid='%sR%sC%s'% (self.shtc__tblname,id,cell)
            if hasattr(self,'shtc__hidecols') and cell in self.shtc__hidecols:
                cellobj=SimpleHtmlCellClass(row[cell],cellid,style='display:none')
            else:
                if hasattr(self,'shtc__evencellstyle') and cell%2==0:
                    cellobj=SimpleHtmlCellClass(row[cell],cellid,self.shtc__evencellstyle)
                elif hasattr(self,'shtc__oddcellstyle') and cell%2!=0:
                    cellobj=SimpleHtmlCellClass(row[cell],cellid,self.shtc__oddcellstyle)
                elif hasattr(self,'shtc__cellstyle'):
                    cellobj=SimpleHtmlCellClass(row[cell],cellid,self.shtc__cellstyle)
                else:
                    cellobj=SimpleHtmlCellClass(row[cell],cellid)
            retval+=str(cellobj)
        if hasattr(self,'shtc__appendables') and type(self.shtc__appendables)==types.ListType:
            cellno=0
            for elem in self.shtc__appendables:
                if cellno==0:
                    cellno=len(row)
                else:
                    cellno=cellno+1
                cellid='%sR%sC%s'% (self.shtc__tblname,id,cellno)
                if self.shtc__processing__headers==False:
                    if hasattr(self,'shtc__cellstyle'):
                        cellobj=SimpleHtmlCellClass(elem,cellid,self.shtc__cellstyle)
                    else:
                        cellobj=SimpleHtmlCellClass(elem,cellid)
                    retval+=str(cellobj)
        retval+="</tr>"
        return retval
    def setcellstyle(self,classname):
        self.shtc__cellstyle=classname
    def setevencellstyle(self,classname):
        self.shtc__evencellstyle=classname
    def setoddcellstyle(self,classname):
        self.shtc__oddcellstyle=classname
    def appendtorow(self,appendables):
        self.shtc__appendables=appendables
    def hidecols(self,cols):
        self.shtc__hidecols=cols
    def drawtable(self,tblname,caption=None):
        self.shtc__tblname=tblname
        if hasattr(self,'shtc__drawpaginated') and self.shtc__drawpaginated:
            if self.shtc__paginate__buttons ==0:
                self.shtc__matter = "<div id = '%s' assoctbl ='%s'> \
                <ul><li id='prev_li'>Previous</li><li id='next_li'>Next</li></ul></div>" % ('paginator',tblname)
            else:    
                self.shtc__matter = "<div id = '%s' assoctbl ='%s'>\
                <ul>\
                <li id='next_li'><img src='/images/next.jpg' alt='next' id='next'/></li>\
                <li id='prev_li'><img src='/images/prev.jpg' alt='previous' id='prev'/></li></ul> \
                </div>" % ('paginator',tblname)
        if self.shtc__matter is None:    
            if hasattr(self,'shtc__tblstyle'):            
                self.shtc__matter="<table name='%s' id='%s' class='%s' cellpadding='0' cellspacing='0' hover>" % (tblname,tblname,self.shtc__tblstyle)
            else:
                self.shtc__matter="<table name='%s' id='%s'>" % (tblname,tblname)
        else:
            if hasattr(self,'shtc__tblstyle'):            
                self.shtc__matter+="<table name='%s' id='%s' class='%s' cellpadding='0' cellspacing='0'>" % (tblname,tblname,self.shtc__tblstyle)
            else:
                self.shtc__matter+="<table name='%s' id='%s'>" % (tblname,tblname)            
        if caption is not None:
            self.shtc__matter+="<caption>%s</caption>" % caption
        if self.shtc__headers is not None:
            self.shtc__matter+="<thead>"
            self.shtc__processing__headers=True
            self.shtc__matter+=self.__drawrow(self.shtc__headers,0)
            self.shtc__processing__headers=False
            self.shtc__matter+="</thead>"
        self.shtc__matter+="<tbody>"
        for row in range(len(self.shtc__payload)):
            self.shtc__matter+=self.__drawrow(self.shtc__payload[row],row+1)
        self.shtc__matter+="</tbody>"
        self.shtc__matter+="</table>"
        return self.shtc__matter
class SimpleHtmlCellClass(object):
    """ A utility class that represents a cell in the  SimpleHtmlTableClass
    """
    def __init__(self,data,id,styleclass=None,style=None):
        self.shcc__data=data
        self.shcc__id=id
        self.shcc__styleclass=styleclass
        self.shcc__style=style
    def __str__(self):
        if self.shcc__styleclass is not None and self.shcc__style is None:
            return "<td class='%s' id='%s'>%s</td>" % (self.shcc__styleclass,self.shcc__id,self.shcc__data)
        elif self.shcc__styleclass is not None and self.shcc__style is not None:
            return "<td class='%s' id='%s' style='%s'>%s</td>" % (self.shcc__styleclass,self.shcc__id,self.shcc__style,self.shcc__data)
        elif self.shcc__styleclass is None and self.shcc__style is not None:
            return "<td id='%s' style='%s'>%s</td>" % (self.shcc__id,self.shcc__style,self.shcc__data)
        else:
            return "<td id='%s'>%s</td>" % (self.shcc__id,self.shcc__data)


if __name__=="__main__":
    tblobj=SimpleHtmlTableClass()
    tblobj.setheaders(['Company Name','Contact Person','Product'])
    tblobj.setpayload([('abc & co','Anil Kapoor','A'),('dec','Anil Kapoor','B'),('der','farooq','Product A')])
    print tblobj.drawtable('datatable')
