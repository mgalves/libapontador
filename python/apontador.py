# -*- coding: utf-8 -*-
# !/usr/bin/python

#################################################################################
# apontador.py
#
# Copyright 2010 Miguel Galves (miguel.galves@lbslocal.com)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http: #www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Requires:
#          OAuth - http://code.google.com/p/oauth/
#          HTTPlib2 - http://code.google.com/p/httplib2/
#
##################################################################################
 
import httplib2
import urllib
import base64
from oauth import oauth 
import time

API_URL = "http://api.apontador.com.br/v1/"


# SEARCH FOR PLACES
SEARCH_PLACES_BY_POINT_URL = API_URL + "search/places/bypoint"
SEARCH_PLACES_BY_ADDRESS_URL = API_URL + "search/places/byaddress"
SEARCH_PLACES_BY_ZIPCODE_URL = API_URL + "search/places/byzipcode"
SEARCH_PLACES_BY_BOX_URL = API_URL + "search/places/bybox"

# PLACES
PLACE_URL = API_URL + "places/%s"
PLACE_PHOTOS_URL = API_URL + "places/%s/photos"
PLACE_REVIEWS_URL = API_URL + "places/%s/reviews"

# CATEGORIES
CATEGORIES_URL = API_URL + "categories"
SUBCATEGORIES_URL = API_URL + "categories/%s/subcategories"
TOP_CATEGORIES_URL = API_URL + "categories/top"

USER_URL = API_URL + "users/self"
USER_PLACES_URL = API_URL + "users/self/places"
USER_PHOTOS_URL = API_URL + "users/self/photos"
USER_REVIEWS_URL = API_URL + "users/self/reviews"

CREATE_NEW_PLACE_URL = API_URL + "places/new"
CREATE_NEW_REVIEW_URL = API_URL + "places/%s/reviews/new"
PLACE_VOTE_UP_URL = API_URL + "places/%s/voteup"
PLACE_VOTE_DOWN_URL = API_URL + "places/%s/votedown"
ADD_PHOTO_TO_PLACE_URL = API_URL + "places/%s/photos/new"

class ApontadorAPI(object):

    def __init__(self, consumer_key=None, consumer_secret=None,
                 oauth_token=None, oauth_token_secret=None):

        # Consumer Key and Secret of the app, used for Basic Auth requests
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
 
        if self._consumer_key and self._consumer_secret:
            base64string = base64.b64encode('%s:%s' % (self._consumer_key, self._consumer_secret))
            self._basic_auth_header =  "Basic %s" % base64string

        # token and secret that allow access to users data. Used for oauth requests
        self._oauth_token = oauth_token
        self._oauth_token_secret = oauth_token_secret

        if self._oauth_token and self._oauth_token_secret:
            self._access_token = oauth.OAuthToken(self._oauth_token, self._oauth_token_secret)
    	else:
            self._access_token = None
            
        self._consumer = oauth.OAuthConsumer(self._consumer_key, self._consumer_secret)
        self._signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        

    def _call_basic_auth_ws(self, url, params):
        if not self._basic_auth_header:
            raise Exception("BASIC HEADER EXCEPTION")
        
        if params:
            querystring = "?"+urllib.urlencode(params)
        else:
            querystring= ""
        
        print url + querystring
        
        http = httplib2.Http()
        response, content = http.request(url+querystring, "GET", headers={"Authorization": self._basic_auth_header})
        if response["status"] != '200':
            raise Exception(response.reason)

        return content
        

    def _call_oauth_ws(self, url, params=None, http_method="GET"):
        oauth_base_params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
            'oauth_consumer_key': self._consumer_key,
            'oauth_token': self._oauth_token
            }
        
        if params:
            params.update(oauth_base_params)
        else:
            params = oauth_base_params
            
        request = oauth.OAuthRequest(http_method=http_method, http_url=url,parameters=params)
        request.sign_request(self._signature_method, self._consumer, self._access_token)

        if http_method == "POST" or http_method == "PUT":
            encoded_post_data = request.to_postdata()
        else:
            url = request.to_url()
            encoded_post_data = ""

        print
        print url
        print
       
        http = httplib2.Http()
        if encoded_post_data:
            response, content = http.request(url,http_method, body=encoded_post_data)
        else:
            response, content = http.request(url, "GET")

        if response["status"] != '200':
            raise Exception(response.reason)

        return content


    def _process_optional_parameters(self, params, **kwargs):
        for key, value in kwargs.iteritems():
            if value:
                params[key] = value
        return params
    
   
    def search_places_by_point(self, latitude, longitude, radius_mt=None,
                            term=None, category_id=None, sort_by=None, order=None,
                            rating=None, page=None, limit=None, user_id=None, type=None):

        params = {"lat": latitude,
                  "lng": longitude}

        self._process_optional_parameters(params, radius_mt=radius_mt,
                                          term=term, category_id=category_id, sort_by=sort_by, order=order,
                                          rating=rating, page=page, limit=limit, user_id=user_id, type=type)
        
        response = self._call_basic_auth_ws(SEARCH_PLACES_BY_POINT_URL, params)
        return response

        
    def search_places_by_address(self, city, state, country=None, street=None, number=None,
                                 district=None, radius_mt=None, term=None, category_id=None,
                                 sort_by=None, order=None, rating=None, page=None, limit=None,
                                 user_id=None, type=None):

        params = {"city": city, "state": state}
        self._process_optional_parameters(params, country=country, street=street, number=number,
                                 district=district, radius_mt=radius_mt, term=term, category_id=category_id,
                                 sort_by=sort_by, order=order, rating=rating, page=page, limit=limit,
                                 user_id=user_id, type=type)
        
        response = self._call_basic_auth_ws(SEARCH_PLACES_BY_ADDRESS_URL, params)
        return response


    def search_places_by_zipcode(self, zipcode, radius_mt=None, term=None, category_id=None,
                                 sort_by=None, order=None, rating=None, page=None, limit=None,
                                 user_id=None, type=None):			

	params = {"zipcode": zipcode}
        self._process_optional_parameters(params, radius_mt=radius_mt, term=term,
                                          category_id=category_id,
                                          sort_by=sort_by, order=order, rating=rating,
                                          page=page, limit=limit,
                                          user_id=user_id, type=type)
        
        response = self._call_basic_auth_ws(SEARCH_PLACES_BY_ZIPCODE_URL, params)
        return response


    def search_places_by_box(self, se_lat, se_lng, nw_lat, nw_lng,
                             term=None, category_id=None, sort_by=None,
                             order=None, rating=None, page=None, limit=None,
                             user_id=None, type=None):

        params = {"se_lat": se_lat, "se_lng": se_lng,
                  "nw_lat": nw_lat, "nw_lng": nw_lng}
        self._process_optional_parameters(params, term=term, category_id=category_id,
                                          sort_by=sort_by, order=order,
                                          rating=rating, page=page, limit=limit,
                                          user_id=user_id, type=type)

        response = self._call_basic_auth_ws(SEARCH_PLACES_BY_BOX_URL, params)
        return response


    def get_place(self, placeid, type=None):
        params = {}
        if type:
            params["type"] = type        
     	url = PLACE_URL%placeid
        response = self._call_basic_auth_ws(url, params)
        return response

    
    def get_place_photos(self, placeid, type=None):
        params = {}
        if type:
            params["type"] = type
     	url = PLACE_PHOTOS_URL%placeid
        response = self._call_basic_auth_ws(url, params)
        return response


    def get_place_reviews(self, placeid, type=None):
        params = {}
        if type:
            params["type"] = type
        url = PLACE_REVIEWS_URL%placeid
        response = self._call_basic_auth_ws(url, params)
        return response


    def get_categories(self, type=None, term=None):
        params = {}
        self._process_optional_parameters(params, type=type, term=term)
        response = self._call_basic_auth_ws(CATEGORIES_URL, params)
        return response


    def get_top_categories(self, type=None):
        params = {}
        if type:
            params["type"] = type
     	response = self._call_basic_auth_ws(TOP_CATEGORIES_URL, params)
        return response

    
    def get_subcategories(self, categoryid, type=None, term=None):
        params = {}
        self._process_optional_parameters(params, type=type, term=term)
        url = SUBCATEGORIES_URL%categoryid
     	response = self._call_basic_auth_ws(url, params)
        return response


    def get_user(self, type=None):
        params = {}
        if type:
            params["type"] = type
     	response = self._call_oauth_ws(USER_URL, params)
        return response


    def get_user_places(self, page=None, limit=None, type=None):
        params = {}
        self._process_optional_parameters(params, type=type, limit=limit, page=page)
        response = self._call_oauth_ws(USER_PLACES_URL, params)
        return response
    

    def get_user_reviews(self, page=None, limit=None, type=None):
    	params = {}
        self._process_optional_parameters(params, type=type, limit=limit, page=page)
        response = self._call_oauth_ws(USER_REVIEWS_URL, params)
        return response


    def create_new_place(self, name=None, address_street=None, address_number=None, address_complement=None,
                         address_district=None, address_city_name=None, address_city_state=None, address_city_country=None,
                         point_lat=None, point_lng=None, phone_country=None, phone_area=None,
                         phone_number=None, category_id=None, subcategory_id=None, description=None,
                         tags=None, icon_url=None, other_url=None, type=None):

     	
        params = {"name": name,
                  "address_street": address_street,
                  "address_number": address_number,
                  "address_district": address_district,
                  "address_city_name": address_city_name,
                  "address_city_state": address_city_state,
                  "category_id": category_id,
                  "subcategory_id": subcategory_id}
        
        self._process_optional_parameters(params, address_complement=address_complement,
                                          address_city_country=address_city_country,
                                          point_lat=point_lat, point_lng=point_lng,
                                          phone_country=phone_country, phone_area=phone_area,
                                          phone_number=phone_number, description=description,
                                          tags=tags, icon_url=icon_url, other_url=other_url, type=type)
        
        response = self._call_oauth_ws(CREATE_NEW_PLACE_URL, params, http_method="PUT")
        return response
    

    def _to_utf(self, message):
        if type(message) == unicode:
            return message.encode("utf-8")
        else:
           return message

            
    def create_new_review(self, place_id, rating, content, type=None):
        params = {"rating": rating,
                  "content": self._to_utf(content)} 
        if type:
            params["type"] = type

        url = CREATE_NEW_REVIEW_URL%place_id
        response = self._call_oauth_ws(url, params, http_method="PUT")
        return response


    def add_photo_to_place(self, place_id, image_file, type=None):
        file = open(image_file, "rb")
        bytes = file.read()
        encoded_bytes = base64.b64encode(bytes)
        
        params = {"content": encoded_bytes}
        if type:
            params["type"] = type

        url = ADD_PHOTO_TO_PLACE_URL%place_id
        response = self._call_oauth_ws(url, params, http_method="PUT")
        return response



    def vote_place_up(self, place_id, type=None):
        params = {}
        if type:
            params["type"] = type
        url = PLACE_VOTE_UP_URL%place_id
        try:
            self._call_oauth_ws(url, params, http_method="PUT")
            return True
        except:
            return False


    def vote_place_down(self, place_id, type=None):
        params = {}
        if type:
            params["type"] = type
        url = PLACE_VOTE_DOWN_URL%place_id
        try:
            self._call_oauth_ws(url, params, http_method="PUT")
            return True
        except:
            return False
    
