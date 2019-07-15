'''Test the behavior of the GmapApi'''

from .models import GmapApi
GMAP = GmapApi()

class TestGmapApi():
    '''Test the behavior of the GmapApi'''

    def test_ouput_type(self):
        '''Test that data are being received or not from Google Map Api'''

        to_locate = [("venise", dict),
                     ("mont saint michel", dict),
                     ("openclassrooms paris", dict),
                     ("cihzsoz", type(None)),
                     ("", type(None))
                     ]
        for entry in to_locate:
            assert type(GMAP.search_address(entry[0])) is entry[1]
