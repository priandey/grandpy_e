'''Object in charge of communication with Gmap API '''

import requests
import os

class GmapApi():
    '''Object in charge of communication with Gmap API '''

    def __init__(self):
        self.api_key = os.environ.get("GMAPKEY")
        self.gmap_place_details = 'https://maps.googleapis.com/maps/api/place/details/json?'
        self.gmap_place = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'


    def search_address(self, parsed_data):
        '''Request to google Map "Place Details" API'''
        payload = {"placeid" : self.search_place_id(parsed_data),
                   "fields" : "address_components,formatted_address,geometry",
                   "key" : self.api_key,
                   "language" : "fr"
                   }
        raw_output = requests.get(self.gmap_place_details, params=payload)
        json_output = raw_output.json()
        if json_output["status"] == "OK":
            passing_keyword = None
            for info in json_output['result']['address_components']:
                if 'route' in info["types"]:
                    passing_keyword = info["short_name"]

            if passing_keyword is None:
                for info in json_output['result']['address_components']:
                    if 'locality' in info["types"]:
                        passing_keyword = info["short_name"]
            to_return = {"address": json_output['result']['formatted_address'],
                         "name": passing_keyword,
                         "lat": json_output['result']["geometry"]['location']['lat'],
                         "long": json_output['result']["geometry"]['location']['lng']
                         }
        else:
            to_return = None
        return to_return

    def search_place_id(self, parsed_data):
        '''Request to google map "Place Api" to get the location ID'''

        payload = {"input" : parsed_data,
                   "inputtype" : 'textquery',
                   "fields" : "place_id",
                   "key" : self.api_key,
                   "language": "fr"
                   }
        raw_output = requests.get(self.gmap_place, params=payload)
        json_output = raw_output.json()
        if json_output["status"] != "ZERO_RESULTS" and json_output['candidates']:
            to_return = json_output["candidates"][0]["place_id"]

        else:
            to_return = None
        return to_return
