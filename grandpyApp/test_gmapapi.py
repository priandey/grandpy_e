'''Test the behavior of the GmapApi'''

import responses

from .models import GmapApi

gmap = GmapApi()

class TestGmapApi():
    '''Test the behavior of the GmapApi'''

    @responses.activate
    def test_correct_output_type(self):
        '''Test that data are being well processed by GmapApi class'''

        responses.add(responses.GET, 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?',
                      json={'candidates': [{'place_id': 'ChIJiT3W8dqxfkcRLxCSvfDGo3s'}], 'status': 'OK'}, status=200)
        responses.add(responses.GET,'https://maps.googleapis.com/maps/api/place/details/json?',
        json={
            'html_attributions': [], 'result': {
            'address_components': [{'long_name': 'Venise', 'short_name': 'Venise', 'types': ['locality', 'political']},
                                   {
                                       'long_name': 'Venise', 'short_name': 'Venise',
                                       'types'    : ['administrative_area_level_3', 'political']
                                   }, {
                                       'long_name': 'Venise', 'short_name': 'VE',
                                       'types'    : ['administrative_area_level_2', 'political']
                                   }, {
                                       'long_name': 'Vénétie', 'short_name': 'Vénétie',
                                       'types'    : ['administrative_area_level_1', 'political']
                                   }, {'long_name': 'Italie', 'short_name': 'IT', 'types': ['country', 'political']}],
            'formatted_address' : 'Venise, Italie', 'geometry': {
                'location': {'lat': 45.4408474, 'lng': 12.3155151}, 'viewport': {
                    'northeast': {'lat': 45.5779746, 'lng': 12.5966574},
                    'southwest': {'lat': 45.23111189999999, 'lng': 12.1668278}
                }
            }
        }, 'status'            : 'OK'
        }, status=200)

        to_locate = [("venise", dict),
                     ("mont saint michel", dict),
                     ("openclassrooms paris", dict),
                     ]
        for entry in to_locate:
            assert type(gmap.search_address(entry[0])) is entry[1]
    @responses.activate
    def test_incorrect_output_types(self):

        responses.add(responses.GET, 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?',
                      json={'candidates': [], 'status': 'ZERO_RESULTS'}, status=200)
        responses.add(responses.GET, 'https://maps.googleapis.com/maps/api/place/details/json?',
                      json={'error_message': 'Missing the placeid or reference parameter.', 'html_attributions': [], 'status': 'INVALID_REQUEST'}, status=200)

        to_locate = [('ojnbd', type(None)),
                     ("", type(None))]

        for entry in to_locate:
            assert type(gmap.search_address(entry[0])) is entry[1]