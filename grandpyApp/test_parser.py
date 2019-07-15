'''Test for methods of DataParser'''

from .models import DataParser

PARSER = DataParser()

class TestParser():
    '''Test for methods of DataParser'''

    def test_kw_parser(self):
        '''Test the parsing of request into keywords'''

        to_parse = [("Parles-moi de Cuzy", "cuzy"),
                    ("Bonjour Grandpy, que sais-tu de Chateaudun ?",
                     "chateaudun"),
                    ("...................", ""),
                    ("127,145,Venise", "venise"),
                    ("", "")]
        for entry in to_parse:
            assert PARSER.kw_parser(entry[0]) == entry[1]

    def test_parse_info(self):
        '''Test the parsing of the data from wikipedia'''

        to_parse = [("Phrase 1. Phrase 2. Phrase 3. Phrase 4",
                     "Phrase 1. Phrase 2. Phrase 3"),
                    ("Phrase 1. Phrase 2.==Cat== Phrase 3. Phrase 4",
                     "Phrase 1. Phrase 2."),
                    (".", "."),
                    ("Phrase 1, Phrase 2, Phrase 3",
                     "Phrase 1, Phrase 2, Phrase 3")]
        for entry in to_parse:
            assert PARSER.info_parser(entry[0]) == entry[1]
