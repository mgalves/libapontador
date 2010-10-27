# -*- coding: utf-8 -*-
from apontador import ApontadorAPI

CONSUMER_KEY = "PUT YOUR CONSUMER KEY HERE"
CONSUMER_SECRET = "PUT YOUR CONSUMER SECRET HERE"
OAUTH_TOKEN = "PUT YOUR OAUTH TOKEN HERE"
OAUTH_TOKEN_SECRET = "PUT YOUR OAUTH TOKEN SECRET HERE"

api = ApontadorAPI(consumer_key = CONSUMER_KEY,
                   consumer_secret = CONSUMER_SECRET,
                   oauth_token = OAUTH_TOKEN,
                   oauth_token_secret = OAUTH_TOKEN_SECRET)

        
######################################################
# Basic Auth calls
######################################################

response = api.search_places_by_point(latitude=-23, longitude=-46, type="json")
print response
print
        
response = api.search_places_by_address(state="SP", city="Campinas", type="json")
print response
print

response = api.search_places_by_zipcode(zipcode="01425-080", type="json")
print response
print

response = api.search_places_by_box(se_lat=-23, se_lng=-42, nw_lat=-20, nw_lng=-48)
print response
print

response = api.get_place("C40367121B481Q4814", type="json")
print response
print

response = api.get_place_photos("C40367121B481Q4814", type="json")
print response
print

response = api.get_place_reviews("C40367121B481Q4814", type="json")
print response
print

response = api.get_categories(type="json")
print response
print

response = api.get_subcategories(categoryid=28, type="json")
print response
print

response = api.get_top_categories(type="json")
print response
print

#################################################################
# OAuth based calls
#################################################################

response = api.get_user(type="json")
print response
print

response = api.get_user_places(type="json")
print response
print

response = api.get_user_reviews(type="json")
print response
print

response = api.get_place_reviews(placeid="C4030843562F2Q2F2E", type="json")
print response
print

response = api.create_new_place(name =  "casa do tonho  %d"%randint(1, 10000),
                                     address_street = "Joao clemente tesseroli",
                                     address_number = "90",
                                     address_district = "JD das americas",
                                     address_city_name = "Curitiba",
                                     address_city_state = "PR",
                                     address_city_country = "BR",
                                     address_complement = "perto do",
                                     point_lat = "",
                                     point_lng = "",
                                     phone_country = "55",
                                     phone_area = "41",
                                     phone_number = "54131154",
                                     category_id = "67",
                                     subcategory_id = "95267",
                                     description = "Local muito legal",
                                     icon_url = "http://maplink.uol.com.br",
                                     other_url = "http://maplink.apontador.com.br",
                                     type="json")

print response
print

response = api.create_new_review(place_id="C4082484225B2C5B21",
                                      rating=randint(1,3),
                                      content="Ótimo local! Recomendo fortemente %d"%randint(1, 10000),
                                      type="json")
print response
print

api.vote_place_up(place_id="C4030843562F2Q2F2E", type="json")
api.vote_place_down(place_id="C4030843562F2Q2F2E", type="json")

print api.add_photo_to_place(place_id="C402650422221N2218", image_file="/tmp/casa5.jpg")
