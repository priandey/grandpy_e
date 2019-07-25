'''Object in charge of communication with wikimedia API'''

import requests
from .dataparser import DataParser

class WikiMediaApi():
    '''Object in charge of communication with wikimedia API'''

    def __init__(self):
        self.url_api = "https://fr.wikipedia.org/w/api.php"
        self.payload = {'action':'query',
                        'generator':'search',
                        'gsrsearch':"",
                        'prop':'extracts',
                        'format':'json',
                        'explaintext':'1',
                        'exlimit':'1',
                        'exchars':'800',
                        'exintro':'1',
                        'gsrsort':'just_match'
                        }

    def get_wikidata(self, keyword):
        '''Request wikimedia for data, and return parsed data'''

        if keyword == "" or keyword is None:
            return None
        keyword = keyword.lower()
        self.payload["gsrsearch"] = keyword
        raw_output = requests.get(self.url_api, params=self.payload)
        json_output = raw_output.json()
        if len(json_output) > 1:
            key_of_extract = list(json_output['query']['pages'].keys())[0]
            if key_of_extract != '-1':
                extract = {'text' : DataParser().info_parser(json_output['query']['pages'][key_of_extract]['extract']),
                           'url' : 'https://fr.wikipedia.org/?curid='+key_of_extract}
                if extract in [".", ""]:
                    extract = None
        else:
            extract = None
        return extract
