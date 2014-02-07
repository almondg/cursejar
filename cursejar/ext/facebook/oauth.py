# May 2012
# Python Facebook Graph API
#
# Written by Gal Hochberg (hochbergg@gmail.com)
#
import os
import urllib2
import urlparse

import simplejson


STATE_RANDOM_SIZE = 14
FACEBOOK_OAUTH_URI = "https://www.facebook.com/dialog/oauth"
FACEBOOK_TOKEN_URI = "https://graph.facebook.com/oauth/access_token"

class OAuthClientException(Exception):
    def __init__(self,msg,reason=None):
        Exception.__init__(self,msg)
        self._reason = reason

class OAuthAuthException(Exception):
    pass

class OAuthClient(object):
    "OAuthClient - Client for OAuth for Facebook"
    def __init__(self,app_id,app_secret,redirect_uri):
        """app_id - APP_ID
        app_secret - APP_SECRET
        redirect_url - redirect url for after the user responds to the dialog. The requests need to be fed into authorize()
        """
        self._app_id = app_id
        self._app_secret = app_secret
        self._redirect_uri = redirect_uri
        
    def request_auth(self,scope):
        """
        Get a request for authorization. Returns a state object for security which needs to be passed to authorize, and a url to redirect the user to
        scope - A list of permissions for the request (can be found at http://developers.facebook.com/docs/authentication/permissions/)
        """
        state = os.urandom(STATE_RANDOM_SIZE).encode("hex")
        return (state,FACEBOOK_OAUTH_URI+"?client_id=%s&redirect_uri=%s&scope=%s&state=%s"%(self._app_id,self._redirect_uri,",".join(scope),state))
    
    def authorize(self,requestItem,state):
        """
        Get an access token from facebook.
        request_uri - URI client was redirected to by facebook
        state - State returned by request_auth()
        
        Returns an access token and an expiry time in seconds
        """
        #If weapp2.request
        if hasattr(requestItem, "request"):
             request = requestItem.request
             #o = urlparse.urlparse("?state=" + request.get("state"))
             qs = {}
             qs["state"] = request.get("state")
             for key,value in request.GET.items():
                 qs[str(key)] = [str(value)]
             requestItem.response.out.write( str(qs) )
        #If simple URI string
        else:
            request_uri = requestItem
            o = urlparse.urlparse(request_uri)
            try:
                qs = urlparse.parse_qs(o.query)
            except Exception, e:
                 raise OAuthClientException("OAuthClient: Could not parse request_uri query string",e)       
        if "state" not in qs:
            raise OAuthClientException("OAuthClient: Bad request_uri on authorize: request uri does not contain state parameter... %s from: %s" %(qs, request_uri))
        
        gotten_state = qs["state"][0]

        if state is not None and gotten_state != state:
            raise OAuthClientException("OAuthClient: Bad request_uri on authorize: passed state does not correspond to saved state. This is a security danger (cross site request forgery, per facebook)")
        
        if "code" in qs:
            # Great Success!
            # Lookup code from server
            try:
                code = qs["code"][0]
                ret = urllib2.urlopen(FACEBOOK_TOKEN_URI+"?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s"%
                                      (self._app_id,self._redirect_uri,self._app_secret,code))
            except urllib2.URLError,e:
                if isinstance(e,urllib2.HTTPError):
                    if e.code >= 400 and e.code < 500:
                        # Facebook api error, parse the json
                        try:
                            # No need to test for edge cases, as all exceptions will be caught by the catchall and thrown up
                            r = simplejson.loads(e.read())
                            er = r["error"]
                            type = er["type"]
                            message = er["message"]
                            raise OAuthAuthException("OAuth (requesting token):  %s: %s"%(type,message),e)
                        except Exception,e: 
                            if isinstance(e,OAuthAuthException):
                                raise
                            # Otherwise, pass
                                        
                raise #OAuthClientException("OAuthClient: Problem requesting token from server",e)
            
            try:
                ret_res = urlparse.parse_qs(ret.read())
            except:
                raise OAuthClientException("OAuthClient: Problem requesting token from server: could not parse response string",e)
            
            if "access_token" not in ret_res:
                raise OAuthClientException("OAuthClient: Problem parsing token from server: token did not contain access_token",e)
            
            if "expires" not in ret_res:
                raise OAuthClientException("OAuthClient: Problem parsing token from server: token did not contain expires",e)
            
            access_token = ret_res["access_token"][0]
            expires = int(ret_res["expires"][0])
            
            try:
                expires = int(expires)
            except:
                raise OAuthClientException("OAuthClient: Problem parsing token from server: could not parse expires",e)
                
            return (access_token,expires)
        
        if "error" in qs:
            e = OAuthAuthException("OAuth: Error in authenticating")
            e.error = qs["error"][0]
            
            if "error_reason" in qs:
                e.error_reason = qs["error_reason"][0]
                
            if "error_description" in qs:
                e.error_description = qs["error_description"][0]
            
            raise e
        
        raise OAuthClientException("OAuthClient: Bad request_uri on authorize: uri does not contain an error or a code and is indeterminate... %s"%qs)        