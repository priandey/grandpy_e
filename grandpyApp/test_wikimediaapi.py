'''Test WikiMediaApi behavior'''
import responses

from .models import WikiMediaApi

WIKIMEDIA = WikiMediaApi()

class TestWikiMediaApi():
    '''Test WikiMediaApi behavior'''

    @responses.activate
    def test_correct_info(self):
        '''
        Test behavior of get_wikidata when receiving a valid set of data
        '''

        responses.add(responses.GET, "https://fr.wikipedia.org/w/api.php",
                      json={'continue': {'excontinue': 1, 'continue': '||'}, 'query': {'pages': {'759146': {'pageid': 759146, 'ns': 0, 'title': 'Arsenal de Venise', 'index': 9, 'extract': "L'arsenal de Venise, onnement (travail à la chaîne)"}, '1950490': {'pageid': 1950490, 'ns': 0, 'title': 'Aéroport de Venise-Marco-Polo', 'index': 10}, '110854': {'pageid': 110854, 'ns': 0, 'title': 'Doge de Venise', 'index': 3}, '3945274': {'pageid': 3945274, 'ns': 0, 'title': 'Histoire de Venise', 'index': 6}, '1766270': {'pageid': 1766270, 'ns': 0, 'title': 'Lagune de Venise', 'index': 4}, '935880': {'pageid': 935880, 'ns': 0, 'title': 'Les Gondoles à Venise', 'index': 5}, '3236165': {'pageid': 3236165, 'ns': 0, 'title': 'Muscat-de-beaumes-de-venise', 'index': 8}, '75687': {'pageid': 75687, 'ns': 0, 'title': 'République de Venise', 'index': 2}, '1063319': {'pageid': 1063319, 'ns': 0, 'title': 'Sestiere (Venise)', 'index': 7}, '8231': {'pageid': 8231, 'ns': 0, 'title': 'Venise', 'index': 1}}}},
                      status=200)

        to_search = ("coucou", dict)

        assert type(WIKIMEDIA.get_wikidata(to_search[0])) is to_search[1]

    @responses.activate
    def test_incorrect_info(self):
        '''
        Test behavior of get_wikidata when receiving an invalid set of data
        '''

        responses.add(responses.GET, "https://fr.wikipedia.org/w/api.php",
                      json={}, status=200)
        to_search = ("ljbef", type(None))
        assert type(WIKIMEDIA.get_wikidata(to_search[0])) is to_search[1]