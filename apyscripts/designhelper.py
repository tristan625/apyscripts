#Shree Ganeshayah Namah

import types

class designhelper(object):
    def __init__(self):
        pass
    """
       @param name:- name of the control
       @param collection:- collection to populate
       @param order:-field order for text and value
       @param selectindex :- index value to be selected in the rendered control
       @param selectedvalue:-value to be selected in the rendered control
       @param accesskey:-accesskey for  the control
       @param style:-inline style statement for the control
       @param taborder:-taborder of the control
       @param hasevent:-we want to associate an event with this control
       @param eventfunct:-function to be called in response to the click event
    """

    def DrawSelect(self, name, collection, order, selectedindex=0, selectedvalue=None, accesskey='p', style=None, taborder=None, hasEvent=False, eventfunc=None, attrs=None):
        keyval = order.split(":")
        matter = "<select name='%s' id='%s' " % (name, name)
        if type(attrs) == types.DictionaryType: # we have a dictionary of attributes add
          for attr in attrs:
              matter += " %s=%s " % (attr, attrs[attr])
        if style  is not None:
            matter += "style='%s'" % style
        if taborder is not None:
            matter += "tabindex='%s'" % taborder
        matter +=">"
        for cnt in range(len(collection)):
            matter += "<option value='"
            if len(keyval) == 1: #we are probably rendering an array
                matter += str(cnt) + "'"
            else:
                matter += str(collection[cnt][int(keyval[1])]) + "'"
            if selectedvalue is not None and len(keyval) != 1 and selectedvalue == collection[cnt][int(keyval[1])]:
                matter += " selected='selected'"
            if selectedvalue is None and int(cnt) == selectedindex:
                matter += " selected='selected'"
            if selectedvalue is not None and len(keyval) == 1 and selectedvalue == cnt:
                matter += " selected='selected'"
            matter += '>'
            if len(keyval) == 1:
                matter += str(collection[int(cnt)])
            else:
                matter += str(collection[int(cnt)][int(keyval[0])])
            matter += "</option>\n"
        matter = matter + '</select>'
        return matter

    def DrawButton(self, name, value):
        matter = "<input type=%s name='%s' value='%s' id='%s'/>" % ('button', \
                                        name, value, name)
        return matter

    def DrawHidden(self, name, value=0):
        matter = "<input type=%s name='%s' value='%s' id='%s'/>" % ('hidden', \
                                        name, value, name)
        return matter
    
    def DrawImage(self, name, src,alt=None):
            matter = "<img name='%s' src='%s' id='%s' alt='%s'/>" % (\
                                            name, src, name, alt if alt is not None else name)
            return matter    

if __name__ == '__main__':
    designobj = designhelper()
    months = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July', \
              'August', 'September', 'October', 'November', 'December']
    # print designobj.DrawSelect('ll', months, "", 0, 2)
    tbldata = [('TDS80MC:5:2','80c'),('TDS80L:2:2','80d')]
    print designobj.DrawSelect('testselect',tbldata,"1:0",0,'TDS80L:2:2')

