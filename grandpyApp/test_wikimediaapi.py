'''Test WikiMediaApi behavior'''

from .models import WikiMediaApi

WIKIMEDIA = WikiMediaApi()

class TestWikiMediaApi():
    '''Test WikiMediaApi behavior'''

    def test_info(self):
        '''Test that data are being received or not from wikipedia'''

        to_search = [("coucou", dict),
                     ("venise", dict),
                     ("mont saint michel", dict),
                     ("cité paradis", dict),
                     ("cihzsoz", type(None)),
                     ("", type(None))
                    ]
        for entry in to_search:
            assert type(WIKIMEDIA.get_wikidata(entry[0])) is entry[1]

    def test_paradis(self):
        '''Test of the user case given'''

        to_assert = "La cité Paradis est une voie publique située"
        assert to_assert in WIKIMEDIA.get_wikidata("Cité Paradis")["text"]
