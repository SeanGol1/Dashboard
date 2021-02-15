from flask import Flask, render_template
import datetime
from idna import unicode
from newsapi import NewsApiClient
import json
import randfacts


app = Flask(__name__)

@app.route('/')
def index():    
    return render_template("index.html", newsstr = getNews(), fact = getFact())

def getFact():
    rfact = randfacts.getFact()
    return rfact

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




if __name__ == "__main__":
    app.run()