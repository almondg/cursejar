# Python Facebook Graph API
# May 2012
#
# Written by Gal Hochberg (hochbergg@gmail.com)
#
# This is used to debug the oauth api and get an access token for debugging use
from facebook.oauth import OAuthClient

execfile("ext/facebook/oauth.py")
import BaseHTTPServer
import shutil

APP_ID = "272038822828356"
APP_SECRET = "gsgsfgsg42t624ba"

FACEBOOK_APP_ID = "533600183421965"
FACEBOOK_APP_SECRET = "2d92754c7f41c59b24cb5dcae308677e"
FACEBOOK_REFERAL = "http://42foo.com:1441" #"http://facezamatch.appspot.com"
FACEBOOK_OAUTH = (FACEBOOK_APP_ID,FACEBOOK_APP_SECRET,FACEBOOK_REFERAL)

def execute_oauth(url):
    class RedirectCatcher(BaseHTTPServer.BaseHTTPRequestHandler):
        path = None
        def do_GET(self):
            self.__class__.path = self.path
    
    server_address = ('', 1441)
    httpd = BaseHTTPServer.HTTPServer(server_address, RedirectCatcher)

    shutil.launch(url)
    httpd.handle_request()
    return RedirectCatcher.path

c = OAuthClient(*FACEBOOK_OAUTH)

print "Authing user..."
state,url = c.request_auth(["user_photos","friends_photos","offline_access","user_likes","friends_likes","publish_actions"])
ret = execute_oauth(url)
token,expires = c.authorize(ret,state)
print token