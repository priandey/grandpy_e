'''Views for grandpyApp'''
import json

from flask import Flask, render_template, request, redirect

from .models import GmapApi, WikiMediaApi, DataParser, WeatherApi


APP = Flask(__name__)
PARSER = DataParser()
GMAP = GmapApi()
WIKIMEDIA = WikiMediaApi()
WEATHER = WeatherApi()

@APP.route('/')
def index():
    '''Index of website'''

    return render_template('index.html')

@APP.route('/', methods=['POST'])
def get_query():
    '''Behavior when receiving query from user'''

    if request.form['improve_kw'] != '':
        PARSER.improve_parser(request.form['improve_kw'].split(" "))

    jsdata = str(request.form['userInput'])
    parsed_data = PARSER.kw_parser(jsdata)
    location = GMAP.search_address(parsed_data)
    if location is not None:
        informations = WIKIMEDIA.get_wikidata(location['name'])
        weather = WEATHER.get_weather({"lat":location["lat"],
                                       "lon":location["long"]})
        if informations is None:
            informations = WIKIMEDIA.get_wikidata(parsed_data)
            if informations is None:
                informations = f"je ne savais pas tout à propos de : {parsed_data} et {location['name']}"
        dict_response = {"address" : location['address'],
                         "coordinates": {"lat":location['lat'],
                                         "long" : location['long']},
                         "information" : informations['text'],
                         "url" : informations['url'],
                         "weather" : weather,
                         "search_terms" : location['name'],
                         "status": "ok"
                         }
        to_return = json.dumps(dict_response)
    else:
        to_return = json.dumps({'status':'error',
                                'kw':parsed_data.split(" ")
                                })
    print(to_return)
    return to_return

@APP.route('/improve', methods=['POST'])
def improve_parser():
    '''Get user input to add in the stop-word List'''

    PARSER.improve_parser(request.form.getlist("kw"))
    return redirect("/")
