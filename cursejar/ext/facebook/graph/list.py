# Python Facebook Graph API
# May 2012
#
# Written by Gal Hochberg (hochbergg@gmail.com)
#
from client import *
from node import *

def GraphListIdLambda(data):
    "Basic lambda for use with GraphPageinatedList that assumes the items represent nodes, and their ids are in the initial result"
    return GraphPtr(data["id"])

class GraphPageinatedList(GraphNode):
    "GraphPageinatedList - Encapsulates a FaceBook Graph API list, allowing lazy fetching of the pages on the list"
    def __init__(self,client,ptr,data={},eager=False,preloaded=False,klass=GraphNode,obj_id_lambda=GraphListIdLambda,item_eager=False,item_preloaded=False):
        """client - GraphClient to make requests through
        ptr - GraphPtr to the list (usually a connection)
        data - Already loaded data
        eager,preloaded - as in GraphNode
        klass - Class for the list items
        obj_id_lambda - Lambda to get the object's GraphPtr from the data returned by querying the list
        item_eager - Whether the items should be eager-loaded
        item_preloaded - Whether the inital data returned about the items is the same as by loading them individually
        """
        self._klass = klass
        self._items = []
        self._l = obj_id_lambda
        self._ie = item_eager
        self._ip = item_preloaded
        GraphNode.__init__(self,client,ptr,data,eager,preloaded)
    
    def _after_load(self):
        self._process()
        
    def _fetch_page(self):
        "Fetch the next page, if there is one"
        if self._next_page is None:
            return False
        else:
            self._populate(self._client.request_url(self._next_page))
            self._process()
            return True
    
    # Overwriting load to add limit= parameter
    # TODO: Remove magic constants
    # TODO: Find nicer way to do this
    def _load(self):
        self._populate(self._client.request_ptr(self._ptr,{"limit":"99999999"}))
        self._loaded = True
        self._after_load()
        
    def _process(self):
        "Process the infromation that was _load()ed and populate the list"
        if hasattr(self,"data"):
            self._items.extend([self._klass(self._client,self._l(d),d,self._ie,self._ip) for d in self.data])
            del self.data # Don't need it hanging around, as we've parsed it
        
        if hasattr(self,"paging") and "next" in self.paging:
            self._next_page = self.paging["next"]
        else:
            self._next_page = None
        
        if hasattr(self,"paging"):
            del self.paging
        
    def __getitem__(self,id):
        if not self._loaded:
            self._load()
            
        # Fetch all pages till we have enough or run out of pages to fetch
        while abs(id) >= len(self._items) and self._fetch_page():
            pass
        
        if abs(id) >= len(self._items):
            raise IndexError("PaginatedList index out of range")
        
        return self._items[id]
        
    def __len__(self):
        "Get the length of the list. This will load all list pages, and might take some time"
        if not self._loaded:
            self._load()
            
        # Fetch all pages
        while self._fetch_page():
            pass

        return len(self._items)
    
    def __iter__(self):
        def iter_pageinated_list(l):
            i = 0
            try:
                while True:
                    yield l[i]
                    i += 1
            except IndexError:
                pass
            
            return
        return iter_pageinated_list(self)
    
    def __repr__(self):
        return "<OpenGraph PageinatedList of %ss>"%(self._klass.__name__)

def GraphTypedPageinatedList(klass=GraphNode,obj_id_lambda=GraphListIdLambda,item_eager=False,item_preloaded=False):
    """Creates a python class representing a GraphPageinatedList that its items are of type <klass>
    See GraphPageinatedList constructor for variable details"""
    class GraphTypedPageinatedList(GraphPageinatedList):
        def __init__(self,client,ptr,data={},eager=False,preloaded=False):
            GraphPageinatedList.__init__(self,client,ptr,data,eager,preloaded,klass,obj_id_lambda,item_eager,item_preloaded)

    return GraphTypedPageinatedList