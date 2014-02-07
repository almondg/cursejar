# Python Facebook Graph API
# May 2012
#
# Written by Gal Hochberg (hochbergg@gmail.com)
#
from objects import *


class Graph(object):
    "Graph - Generic entry point to the graph API allowing requests of objects by ID and returning the right object back based on metadata"
    def __init__(self, token):
        self._token = token
        self._c = GraphClient(token)
        
    def get(self,id):
        ptr = GraphPtr(id)
        r = self._c.request_url(ptr.to_url(self._token),{"metadata":"1"})

        t = GraphNode
        if r["type"] in self.types:
            t = self.types[r["type"]]
        
        return t(self._c,ptr,r,preloaded=True)
        
    
    types = {"user": User, "photo": Photo, "album": Album, "post": Post, "comment": Comment}
         