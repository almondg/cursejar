# Python Facebook Graph API
# May 2012
#
# Written by Gal Hochberg (hochbergg@gmail.com)
#
# This is used to debug the graph wrapper
import graph.client
import graph.node
import graph.list
import graph.fields
import graph.objects
import graph.graph

reload(graph)
reload(graph.client)
reload(graph.node)
reload(graph.list)
reload(graph.fields)
reload(graph.objects)
reload(graph.graph)
reload(graph)

execfile("oauth_test.py")
g = graph.Graph(token)
u = g.request("me")
f = u.friends
        