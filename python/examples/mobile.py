# Library modules
import urlparse
from oauth import oauth
import httplib2
import urllib
import base64
import time

REQUEST_TOKEN_URL = 'http://api.apontador.com.br/v1/oauth/request_token'
ACCESS_TOKEN_URL = 'http://api.apontador.com.br/v1/oauth/access_token'
AUTHORIZATION_URL = 'http://api.apontador.com.br/v1/oauth/authorize'

SIGNATURE_METHOD = oauth.OAuthSignatureMethod_HMAC_SHA1()

def request(url, params=None, consumer=None, token=None):
        oauth_params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
            'oauth_consumer_key': consumer.key,
            }

        if token:
            oauth_params['oauth_token'] = token.key
            
        if params:
           oauth_params.update(params)

        request = oauth.OAuthRequest(http_method="GET", http_url=url,parameters=oauth_params)
        request.sign_request(SIGNATURE_METHOD, consumer, token)
	url = request.to_url()
	encoded_post_data = ""
       
        http = httplib2.Http()
        if encoded_post_data:
            response, content = http.request(url,http_method, body=encoded_post_data)
        else:
            response, content = http.request(url, "GET")

        return response, content

    
if __name__ == "__main__":
    consumer_key =   raw_input("CONSUMER KEY? ")
    consumer_secret =  raw_input("CONSUMER_SECRET? ")

    consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
    signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

    # REQUEST
    resp, content = request(REQUEST_TOKEN_URL, params={}, consumer=consumer, token=None)
    if resp['status'] != '200':
	    print content
	    raise Exception("Invalid response %s." % resp['status'])
    token_dict = dict(urlparse.parse_qsl(content))
    token = oauth.OAuthToken(token_dict['oauth_token'], token_dict['oauth_token_secret'])
    
    # AUTHORIZATION
    client = oauth.OAuthClient(consumer, token)
    resp, content =  request(AUTHORIZATION_URL, params={}, consumer=consumer, token=token)
    if resp['status'] != '200':
            print content
            raise Exception("Invalid response %s." % resp['status'])
    print("Paste this URL in your Browser: "+content)

    # ACCESS
    # Get the pin # from the user and get our permanent credentials                                                                          
    verifier = raw_input('PIN? ')
    resp, content = request(ACCESS_TOKEN_URL, params={"oauth_verifier": verifier}, consumer=consumer, token=None)
    if resp['status'] != '200':
            print content
            raise Exception("Invalid response %s." % resp['status'])
    access_token = dict(urlparse.parse_qsl(content))

    print("YOUR OAUTH TOKEN: " + access_token['oauth_token'])
    print("YOUR OAUTH TOKEN SECRET: " + access_token['oauth_token_secret'])
