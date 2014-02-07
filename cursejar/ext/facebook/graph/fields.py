from list import *

# TODO: Isn't this just a more specific type of GraphNodeField? (Except it doesnt create GraphNode's but anything you want)
class GraphLazyField(object):        
    "GraphLazyField - a field that isn't returned by loading the object and must be queried individually"
    def __init__(self,field,klass=lambda o:o):
        self._field = field
        self._klass = klass
        
    def __get__(self,obj,objtype=None):
        if obj is None:
            return self
        
        ptr = GraphPtr(obj._ptr.id,obj._ptr.connection,self._field)
        client = obj._client
        
        if not hasattr(obj,"_"+self._field):
            data = client.request_ptr(ptr)
            value = data[self._field] # Because if you request by field, you still get a dict with the field in it
            setattr(obj,"_"+self._field,self._klass(value)) 
            
        return getattr(obj,"_"+self._field) 

    def __set__(self,obj,value):
        setattr(obj,"_"+self._field,value)
        
# Python Facebook Graph API
# May 2012
#
# Written by Gal Hochberg (hochbergg@gmail.com)
#
def GraphNodeFieldIdLambda(obj,data):
    "Lambda for use with GraphNodeField to get the field's ID"
    return GraphPtr(data["id"])

def GraphNodeFieldConnectionLambda(connection):
    "Lambda for use with GraphNodeField to get the pointer to a connection"
    def GraphNodeFieldConnectionLambda(obj,data):
        return GraphPtr(obj.id,connection)
    return GraphNodeFieldConnectionLambda


class GraphNodeField(object):
    "GraphNodeField - Represents a field on a graph node that is a pointer to another graph node"
    def __init__(self,field,klass=GraphNode,eager=False,preloaded=False,ptr_lambda=GraphNodeFieldIdLambda):
        """field - The Field name
        klass - The pointed-at object's type
        eager,preloaded - As in GraphNode
        ptr_lambda - Lambda to get the GraphPtr to the pointed-at object"""
        self._field = field
        self._klass = klass
        self._eager = eager
        self._preloaded = preloaded
        self._nl = ptr_lambda
        
    def __get__(self,obj,objtype=None):
        if obj is None:
            return self

        already_resolved = hasattr(obj,"_"+self._field+"_resolved") and getattr(obj,"_"+self._field+"_resolved") 
        
        if not hasattr(obj,"_"+self._field) or not already_resolved:
            data = {}
            if hasattr(obj,"_"+self._field):
                data = getattr(obj,"_"+self._field)
                
            ptr = self._nl(obj,data)
            client = obj._client
                
            setattr(obj,"_"+self._field,self._klass(client,ptr,data,self._eager,self._preloaded))
            setattr(obj,"_"+self._field+"_resolved",True)
            
        return getattr(obj,"_"+self._field) 

    def __set__(self,obj,value):
        setattr(obj,"_"+self._field,value)
        
class GraphConnection(GraphNodeField):
    "GraphConnection - GraphNodeField built for Facebook Graph API connections (friends, photos, etc)"
    def __init__(self,connection,item_klass=GraphNode,item_eager=False,item_preloaded=False,eager=False,preloaded=False):
        GraphNodeField.__init__(self,connection,GraphTypedPageinatedList(item_klass,item_eager=item_eager,item_preloaded=item_preloaded),eager,preloaded,GraphNodeFieldConnectionLambda(connection))
        
    