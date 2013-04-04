#Shree Ganeshayah Namah

import urllib2,urllib,types
#from win32api import *
#from win32con import *
##from twisted.internet import reactor
##from twisted.web import client
class remoteio:
    """Class to fetch data from Tally running on a
    specified host and port."""

    def __init__(self,host="localhost",port=9000):
        self.__host=host
        self.__port=port
        self.__resource=''
        self.__default__failure__reason=''
        self.__useproxy=False
        self.__proxy__url=None
        self.__proxy__uname=None
        self.__proxy__password=None
        self.__proxy__authtype="basic"
        self.__twisted__matter=None

    def getdata(self,reqdata=None,isformdata=False,issecure=False):
        """Retrieve Remote Data from Tally."""
        f=None
        proxy_handler=None
        proxy_auth_handler=None
        opener=None
        try:
            if self.__useproxy==True:
                if self.__proxy__url.find(":")==-1:
                    self.__proxy__url=self.__proxy__url + ":80"
                if not issecure and not self.__proxy__url.startswith("http://"):
                    self.__proxy__url="http://" + self.__proxy__url
                if issecure and not self.__proxy__url.startswith("https://"):
                    self.__proxy__url="https://" + self.__proxy__url                    
                if issecure:                
                    proxy_handler=urllib2.ProxyHandler({'https': self.__proxy__url})
                else:
                    proxy_handler=urllib2.ProxyHandler({'http': self.__proxy__url})
                if self.__proxy__uname!=None and self.__proxy__password!=None:
                    #proxy_handler=urllib2.ProxyHandler({'http': self.__proxy__url})
                    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
                    password_mgr.add_password(None, self.__proxy__url, self.__proxy__uname, self.__proxy__password)
                    self.guessproxyauth()
                    if self.__proxy__authtype=="basic":
                        if self.__proxy__uname==None or self.__proxy__password==None:
                            self.__default__failure__reason="Username/Password Not Provided"
                            return None
                        proxy_auth_handler=urllib2.ProxyBasicAuthHandler(password_mgr)
                    elif self.__proxy__authtype=="digest":
                        if self.__proxy__uname==None or self.__proxy__password==None:
                            self.__default__failure__reason="Username/Password Not Provided"
                            return None
                        proxy_auth_handler=urllib2.ProxyDigestAuthHandler(password_mgr)
                    elif self.__proxy__authtype=="noauth":
                        proxy_auth_handler=None
                    else:
                        self.__default__failure__reason="Proxy Authentication Type Not Supported"
                        return None
                if proxy_auth_handler!=None:
                    opener = urllib2.build_opener(proxy_handler, proxy_auth_handler)
                else:
                    opener = urllib2.build_opener(proxy_handler)
                urllib2.install_opener(opener)
            else:
                proxy_handler=urllib2.ProxyHandler({})
                opener = urllib2.build_opener(proxy_handler)
                urllib2.install_opener(opener)
            if not isformdata:
                f=urllib2.urlopen(self.__formurl(),reqdata)
            elif isformdata==True and type(reqdata)in [types.TupleType ,types.DictType]:
                if issecure==True:
                    f=urllib2.urlopen(self.__formurl(2),urllib.urlencode(reqdata))
                else:
                    f=urllib2.urlopen(self.__formurl(),urllib.urlencode(reqdata))
            matter=f.read(-1)
            return matter
        except urllib2.URLError,e:
            if hasattr(e,'code'):
                if e.code==407 or e.code==401:
                    self.__default__failure__reason=str(e.code)
                else:
                    self.__default__failure__reason=str(e.code)
            else:
                self.__default__failure__reason=str(e)
            return None
        except urllib2.HTTPError, e:
            self.__default__failure__reason=str(e)
            return None
        except urllib2.httplib.HTTPException, e:
            self.__default__failure__reason=str(e)
            return None
        except Exception,e:
            if hasattr(e,'reason'):
                self.__default__failure__reason=str(e.reason)
                return None
            elif hasattr(e,'code'):
                self.__default__failure__reason=str(e.code)
                return None
            else:
                self.__default__failure__reason=str(e)
                return None
        finally:
            if f!=None:
                pass
##                f.close()
    def __formurl(self,type=1):
        if type==1:
            scheme="http://"
        elif type==2:
            scheme="https://"
        if self.__resource!=None:
            url=scheme + self.__host + ':' + str(self.__port) + "/" + self.__resource
        else:
            url=scheme + self.__host + ':' + str(self.__port)
        return url
    
    def guessproxyauth(self,reqdata=None):
        proxy_handler=None
        f=None
        try:
            if self.__proxy__url.find(":")==-1:
                self.__proxy__url=self.__proxy__url + ":80"
            if not self.__proxy__url.startswith("http://"):
                self.__proxy__url="http://" + self.__proxy__url
            proxy_handler=urllib2.ProxyHandler({'http': self.__proxy__url})
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
            f=urllib2.urlopen(self.__formurl(),reqdata)
            f.read(-1)
            self.__proxy__authtype="noauth"
        except urllib2.URLError,e:
            if hasattr(e,'code'):
                if e.code==407 or e.code==401:
                    if e.hdrs.dict.has_key('proxy-authenticate'):
                        self.__proxy__authtype=self.__getscheme(e.hdrs.dict['proxy-authenticate'])
                        return None
                else:
                    self.__proxy__authtype="noauth"
                    self.__default__failure__reason=str(e.code)
            return None
        except urllib2.HTTPError, e:
            self.__default__failure__reason=str(e)
            return None
        except urllib2.httplib.HTTPException, e:
            self.__default__failure__reason=str(e)
            return None
        except Exception,e:
            if hasattr(e,'reason'):
                self.__default__failure__reason=str(e.reason)
                return None
            elif hasattr(e,'code'):
                self.__default__failure__reason=str(e.code)
                return None
            else:
                self.__default__failure__reason=str(e)
                return None
        finally:
            if f!=None:
                f.close()
    def __getscheme(self,header):
        header=header.lower()
        return header[:header.find("realm")-1]
    def setconnectionparams(self,host='localhost',port=9000,resource=None):
        self.__host=host
        self.__port=port
        self.__resource=resource
    def setproxyparams(self,url,uname=None,passwd=None):
        self.__useproxy=True
        self.__proxy__url=url
        self.__proxy__uname=uname
        self.__proxy__password=passwd
    def getlasterror(self):
        return self.__default__failure__reason

    def getdataviarequestobj(self,reqdata=None,isformdata=False,issecure=False,headers=None,returnmeta=False):
        """Retrieve Remote Data from Tally."""
        f=None
        reqobj=None
        proxy_handler=None
        proxy_auth_handler=None
        opener=None
        try:
            if self.__useproxy==True:
                if self.__proxy__url.find(":")==-1:
                    self.__proxy__url=self.__proxy__url + ":80"
                if not issecure and not self.__proxy__url.startswith("http://"):
                    self.__proxy__url="http://" + self.__proxy__url
                if issecure and not self.__proxy__url.startswith("https://"):
                    self.__proxy__url="https://" + self.__proxy__url                    
                if issecure:                
                    proxy_handler=urllib2.ProxyHandler({'https': self.__proxy__url})
                else:
                    proxy_handler=urllib2.ProxyHandler({'http': self.__proxy__url})
                if self.__proxy__uname!=None and self.__proxy__password!=None:
                    #proxy_handler=urllib2.ProxyHandler({'http': self.__proxy__url})
                    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
                    password_mgr.add_password(None, self.__proxy__url, self.__proxy__uname, self.__proxy__password)
                    self.guessproxyauth()
                    if self.__proxy__authtype=="basic":
                        if self.__proxy__uname==None or self.__proxy__password==None:
                            self.__default__failure__reason="Username/Password Not Provided"
                            return None
                        proxy_auth_handler=urllib2.ProxyBasicAuthHandler(password_mgr)
                    elif self.__proxy__authtype=="digest":
                        if self.__proxy__uname==None or self.__proxy__password==None:
                            self.__default__failure__reason="Username/Password Not Provided"
                            return None
                        proxy_auth_handler=urllib2.ProxyDigestAuthHandler(password_mgr)
                    elif self.__proxy__authtype=="noauth":
                        proxy_auth_handler=None
                    else:
                        self.__default__failure__reason="Proxy Authentication Type Not Supported"
                        return None
                if proxy_auth_handler!=None:
                    opener = urllib2.build_opener(proxy_handler, proxy_auth_handler)
                else:
                    opener = urllib2.build_opener(proxy_handler)
                urllib2.install_opener(opener)
            else:
                proxy_handler=urllib2.ProxyHandler({})
                opener = urllib2.build_opener(proxy_handler)
                urllib2.install_opener(opener)
            if not isformdata:
                if not issecure and not headers:
                    reqobj=urllib2.Request(self.__formurl())
                elif issecure and headers:
                    reqobj=urllib2.Request(self.__formurl(2), headers)
                elif not issecure and headers:
                    reqobj=urllib2.Request(self.__formurl(), headers)
                else:
                    reqobj=urllib2.Request(self.__formurl(2))
                reqobj.add_data(reqdata)
                #reqobj.add_header("Content-Type","text/xml; charset=utf-16")
                f=urllib2.urlopen(reqobj)
            elif isformdata==True and type(reqdata)in [types.TupleType ,types.DictType]:
                if not issecure and not headers:
                    reqobj=urllib2.Request(self.__formurl(),urllib.urlencode(reqdata))
                elif issecure and headers:    
                    reqobj=urllib2.Request(self.__formurl(2),urllib.urlencode(reqdata),headers)
                elif not issecure and headers:    
                    reqobj=urllib2.Request(self.__formurl(),urllib.urlencode(reqdata),headers)
                else:
                    reqobj=urllib2.Request(self.__formurl(2),urllib.urlencode(reqdata))
                f=urllib2.urlopen(reqobj)
            matter=f.read(-1)
            if not returnmeta:
                return matter
            elif returnmeta and matter is  not None:
                return [matter,f.info()]
            else:
                return matter
        except urllib2.URLError,e:
            if hasattr(e,'code'):
                if e.code==407 or e.code==401:
                    self.__default__failure__reason=str(e.code)
                else:
                    self.__default__failure__reason=str(e.code)
            else:
                self.__default__failure__reason=str(e)
            return None
        except urllib2.HTTPError, e:
            self.__default__failure__reason=str(e)
            return None
        except urllib2.httplib.HTTPException, e:
            self.__default__failure__reason=str(e)
            return None
        except Exception,e:
            if hasattr(e,'reason'):
                self.__default__failure__reason=str(e.reason)
                return None
            elif hasattr(e,'code'):
                self.__default__failure__reason=str(e.code)
                return None
            else:
                self.__default__failure__reason=str(e)
                return None
#        finally:
#            if f!=None:
#                f.close()

if __name__=='__main__':
    remobj=remoteio()
    #remobj.setproxyparams("172.16.10.1:3128")
    remobj.setconnectionparams("59.163.46.2",443,"TIN/PanInquiryBackEnd")
    p=remobj.getdata({'data':'V0000501^AASPA5467J^AAAPM3212X'},isformdata=True,issecure=True)

    #remobj.setconnectionparams("localhost",80)
    #remobj.setproxyparams("adi-PC:3128","adi","meenakshi")
    if p==None:
        print remobj.getlasterror()
