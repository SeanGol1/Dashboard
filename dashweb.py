from flask import Flask, render_template
import datetime
from idna import unicode
from newsapi import NewsApiClient
import json
import randfacts
import requests
from random_word import RandomWords

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():    
    return render_template("index.html", newsstr = getNews(), fact = getFact(), country = "", word = getWord())

def getFact():
    rfact = [randfacts.getFact(),randfacts.getFact(),randfacts.getFact()]
    
    return rfact

def getSurf():
    response = requests.get("http://magicseaweed.com/api/YOURAPIKEY/forecast/?spot_id=10&units=eu")
    return response.json()

class Word:
    def __init__(self, w, t):
        self.word = w
        self.text = t    

def getWord():
    r = RandomWords()
    
    rw = r.get_random_word()
    wd = r.word_of_the_day()
    wordtxt = ''
    deftxt = ''
    #for items in wd:
        #wordtxt = items
        #for definations in wd:
            #if(items == 'text'):
                #deftxt += definations['text']
                

    return rw

class NewsStory:
    def __init__(self, t, c):
        self.title = t
        self.content = c
def getNews():
    
    newsapi = NewsApiClient(api_key='94454bdacf3247a2957f23c8de7f597f')

    ########  Irish Headlines
        # Top Irish headlines
    irish_headlines = newsapi.get_top_headlines(country='ie')
    irishList = []
    for items in irish_headlines:
        if(items == 'articles'):
            for articles in irish_headlines[items]:                
                irishList.append ( NewsStory(articles['title'],articles['content']))  


    ########  Tech Headlines
                # Top Tech headlines
    tech_headlines = newsapi.get_top_headlines(sources='mashable,techcrunch.com')
    techList = [];
    for items in tech_headlines:
         if(items == 'articles'):
             for articles in tech_headlines[items]:                
                 techList.append( NewsStory(articles['title'],articles['content']))                 

    return techList , irishList

def getCountry():
    response = requests.get("https://restcountries.eu/rest/v2/region/asia")
    return response.json()


if __name__ == "__main__":
    app.run()