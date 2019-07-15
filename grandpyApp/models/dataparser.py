'''Object parsing user input and data input'''

import os.path

class DataParser():
    '''Object parsing user input and data input'''

    def __init__(self):
        ponctuation = "!\"#$%&'()*+,./:;<=>?@[\\]^_-`{|}~1234567890"
        replace = " " * len(ponctuation)
        self.translation_map = str.maketrans(ponctuation, replace)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.stpword_file = os.path.join(base_dir, 'stop_words')
        self.stop_words = list()

        with open(self.stpword_file, "r") as file:
            for line in file:
                self.stop_words.append(line.replace("\n", ""))

    def kw_parser(self, user_input):
        '''Parse user input into keywords'''

        to_parse = user_input.translate(self.translation_map)
        input_words = to_parse.split(" ")
        output_words = list()
        newlist = list()

        for word in input_words:
            curated_word = word
            if curated_word != '':
                output_words.append(curated_word.lower())
        for entry in output_words:
            if entry in self.stop_words:
                continue
            else:
                newlist.append(entry)
        return " ".join(newlist)

    def info_parser(self, wiki_data):
        '''Parse wikipedia input into short text'''

        intro = wiki_data.split("=")[0]
        phrases = intro.split(".")
        result = ".".join(phrases[0:3])
        return result

    def improve_parser(self, stp_word):
        '''add stp_word to stp_word list'''

        for word in stp_word:
            self.stop_words.append(word)

        with open(self.stpword_file, "a", encoding='utf-8') as file:
            for word in stp_word:
                file.write(word + "\n")
