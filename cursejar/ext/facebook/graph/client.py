# Python Facebook Graph API
# May 2012
#
# Written by Gal Hochberg (hochbergg@gmail.com)
#
import urllib2
import posixpath
import sys

import simplejson


GRAPH_URL = "https://graph.facebook.com/"

class GraphException(Exception):
    """FaceBook Graph API Exception"""
    def __init__(self,msg,reason=None):
        Exception.__init__(self,msg)
        self.reason = reason
        
class GraphClientException(Exception):
    """GraphClient Exception (thrown when there is problem with transporting information)"""
    def __init__(self,msg,reason=None):
        Exception.__init__(self,msg)
        self.reason = reason

class GraphPtr(object):
    """Pointer to a graph node, a node's field or a node's connection."""
    
    def __init__(self,id,connection=None,field=None):
        """id - Required, the node id
        connection - Optional, the requested connection to the node with id <id>
        field - Optional, the field on the object with id <id>"""
        self.id = id
        self.connection = connection
        self.field = field
        
    def to_url(self,token):
        "Convert the GraphPtr to a url"
        if self.connection is None:
            url = posixpath.join(GRAPH_URL,self.id)
        else:
            url = posixpath.join(GRAPH_URL,self.id,self.connection)
        
        url += "?access_token=%s"%token
        if self.field != None:
            url += "&fields="+self.field
        
        return url
    
    def __repr__(self):
        out = "<GraphPtr id: %s"%self.id
        if self.connection != None:
            out += " connection: %s"%self.connection
        if self.field != None:
            out += "field: %s"%self.field
        out += ">"
        return out

class GraphClient(object):
    "GraphClient - A client to facebook's graph API"
    def __init__(self,token):
        "token - A valid access token"
        self._token = token
    
    def request_ptr(self,ptr,params=None,data=None):
        "Request the value behind a pointer on the graph API"
        return self.request_url(ptr.to_url(self._token),params,data)
    
    # TODO: URLEncode anyone?
    def request_url(self,url,params=None,data=None):
        "Request a URL and parse the json result"
        if not params is None:
            url += "&"+"&".join(map(lambda i: i[0]+"="+i[1].replace(" ","+"), params.items()))
            
        print >>sys.stderr, "DEBUG: Requesting URL:",url
        
        try:
            if not data is None:
                ret = urllib2.urlopen(url,data)
            else:
                ret = urllib2.urlopen(url)
            
        except Exception,e:
            if isinstance(e,urllib2.HTTPError):
                if e.code >= 400 and e.code < 500:
                    # Facebook api error, parse the json
                    try:
                        # No need to test for edge cases, as all exceptions will be caught by the catchall and thrown up
                        r = simplejson.loads(e.read())
                        er = r["error"]
                        type = er["type"]
                        message = er["message"]
                        raise GraphException("OpenGraph: %s: %s"%(type,message),e)
                    except Exception,e:
                        if isinstance(e,GraphException):
                            raise
                        # Otherwise, pass

            print e
            raise GraphClientException("OpenGraphClient: Exception making request",e)
        
        try:
            js = simplejson.loads(ret.read())
        except:
            raise GraphClientException("OpenGraphClient: Could not parse result",e)
        
        return js
