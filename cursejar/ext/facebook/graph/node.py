# Python Facebook Graph API
# May 2012
#
# Written by Gal Hochberg (hochbergg@gmail.com)
#
class GraphNode(object):
    "GraphNode - A container for data on the facebook graph API. Supports lazy loading"
    def __init__(self,client,ptr,data={},eager=False,preloaded=False):
        """client - GraphClient to send requests via
        ptr - GraphPtr to the node
        data - Preloaded data about the object (dictionary)
        eager - Whether to fetch the object as it is constructed or fetch it lazily
        preloaded - Whether data represents all the information that will be gotten by loading,
            and therefore the object should be treated as already loaded"""
        self.id = ptr.id # This is here because we always know the object's ID or its connection parent or field parent id, and this is a consistent place to put it
        self._populate(data)
        self._ptr = ptr
        self._client = client
        
        if eager and not preloaded:
            self._load()
            
        self._loaded = preloaded or eager
        
        if preloaded:
            self._after_load()
            
    def _after_load(self):
        "Called after the object is loaded. Should be overridden"
        pass
    
    def _populate(self,data):
        "Populates the object with the items in data"
        for k,v in data.items():
            setattr(self,k,v)
            
    def _load(self):
        "Loads the object by querying the graph API"
        self._populate(self._client.request_ptr(self._ptr))
        self._loaded = True
        self._after_load()
    
    def __getattribute__(self,x):                    
        # Underscores can't be info from facebook, so don't try loading
        if x[0] == "_":
            return object.__getattribute__(self,x)
        
        # First, try to just get the attribute
        try:
            return object.__getattribute__(self,x)
        except AttributeError:
            pass
        
        # If that doesnt work, load it.
        if not self._loaded:
            try:
                # Try looking it up in the unloaded object
                return object.__getattribute__(self,x)
            except AttributeError:
                pass
        
            # Or load  the object if we have to
            self._load()
        
        return object.__getattribute__(self,x) # This wont recurse now that we're loaded

