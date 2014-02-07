# Python Facebook Graph API
# May 2012
#
# Written by Gal Hochberg (hochbergg@gmail.com)
#
from fields import *

class User(GraphNode):
    def __repr__(self):
        return "<Graph User %s (%s)>"%(self.name,self.id)
    
    def post_message_on_wall(self,message):
        "Post a message to the user's wall"
        self._client.request_ptr(GraphPtr(self.id,"feed"),data="message="+message)
    
    def post_link_to_wall(self,link,**kwargs):
        "Post a link to the user's wall"
        params = ["picture","name","caption","description"]
        ndict = dict([(k,v) for k,v in kwargs.items() if k in params])
        ndict["link"] = link
        self._client.request_ptr(GraphPtr(self.id,"feed"),data="&".join([k+"="+v.replace(" ","+") for k,v in ndict.items()]))
    
class Photo(GraphNode):
    def __init__(self,client,ptr,data={},eager=False,preloaded=False):
        GraphNode.__init__(self,client,ptr,data,eager,preloaded)
        self._from = getattr(self,"from") # Because "from" cannot be used in the A.B syntax, and this way it'll seed the data for the GraphNodeField
        delattr(self,"from") # So it wont clutter __dict__
                     
    def __repr__(self):
        return "<Graph Photo %s By %s >"%(self.id,self.from_.name)

class Comment(GraphNode):
    def __init__(self,client,ptr,data={},eager=False,preloaded=False):
        GraphNode.__init__(self,client,ptr,data,eager,preloaded)
        self._from = getattr(self,"from") # Because "from" cannot be used in the A.B syntax, and this way it'll seed the data for the GraphNodeField
        delattr(self,"from") # So it wont clutter __dict__
        
        # TODO: Make the likes field just set the like's pageinated list len(), and not use an extra field
        self.num_likes = getattr(self,"likes") # Facebook chose to have a likes field for number of likes and a likes connection for the acutal likes. This is inconvenient
        # Dont delete "likes" because it'll be defined as relation later
    
    def __repr__(self):
        return "<Graph Comment %s by %s>"%(self.id,self.from_.name)
    
class Album(GraphNode):
    def __init__(self,client,ptr,data={},eager=False,preloaded=False):
        GraphNode.__init__(self,client,ptr,data,eager,preloaded)
        self._from = getattr(self,"from") # Because "from" cannot be used in the A.B syntax, and this way it'll seed the data for the GraphNodeField
        delattr(self,"from") # So it wont clutter __dict__
        
    def __repr__(self):
        return "<Graph Album %s by %s>"%(self.id,self.from_.name)
    
    
class Post(GraphNode):
    def __init__(self,client,ptr,data={},eager=False,preloaded=False):
        GraphNode.__init__(self,client,ptr,data,eager,preloaded)
        self._from = getattr(self,"from") # Because "from" cannot be used in the A.B syntax, and this way it'll seed the data for the GraphNodeField
        delattr(self,"from") # So it wont clutter __dict__
        
    def __repr__(self):
        return "<Graph Post %s by %s>"%(self.id,self.from_.name)
    
# Connections and fields are declared last to allow cross object references

# User 
User.third_party_id = GraphLazyField("third_party_id")
User.picture = GraphLazyField("picture")   
User.friends = GraphConnection("friends",User)
User.likes = GraphConnection("likes")
User.photos = GraphConnection("photos",Photo,item_preloaded=True)
User.albums = GraphConnection("albums",Album,item_preloaded=True)
User.posts = GraphConnection("posts",Post)

# Photo
Photo.from_ = GraphNodeField("from",User)
Photo.tags = GraphConnection("tags")
Photo.comments = GraphConnection("comments",Comment,item_preloaded=True,preloaded=True)

# Comment
Comment.from_ = GraphNodeField("from",User)
Comment.likes = GraphConnection("likes",User)

# Album
Album.from_ = GraphNodeField("from",User)
Album.photos = GraphConnection("photos",Photo,item_preloaded=True)
Album.comments = GraphConnection("comments",Comment,item_preloaded=True)
Album.likes = GraphConnection("likes",User)

# Post
Post.from_ = GraphNodeField("from",User)