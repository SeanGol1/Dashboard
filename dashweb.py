from flask import Flask, render_template,jsonify
from datetime import datetime
from idna import unicode
from newsapi import NewsApiClient
import json
import randfacts
import tmdbsimple as tmdb
import requests
from random_word import RandomWords
import random
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    
    #loadPage('')
    #stock = getStock()
    return render_template("index.html", coun = getCountry(),tvguide = getTVGuide(), time = getDate(), newsstr = getNews(),  fact = getFact(), newscount = 0, word = getWord())

def loadPage(searchData):
    
    return render_template("index.html", coun = getCountry(), newsstr = getNews(), fact = getFact(), searchnews = searchData, newscount = 0, word = getWord())

def getTVGuide():
    data_fetch = True
    pages = ['&page=1', '&page=2', '&page=3']
    count = 0
    todays_shows = []
    our_shows = []
    favourites = ['Superman & Lois', 'Emmerdale', 'WWE Raw','The Good Doctor']

    for items in pages:

        if count >= 3:
            break
        
        page_number = pages[0]

        tmdb.api_key = "74d5287b6bd749f76603010fdcf24585"   
        url = "https://api.themoviedb.org/3/tv/airing_today?api_key=74d5287b6bd749f76603010fdcf24585&language=en-US"+str(items)
        count += 1


        request = requests.get(url)
        json = request.json()
           
        for i in json.get('results'):
            y = i["name"]
            if y in favourites:
                todays_shows.append(y)

      
    return todays_shows
        
    
    
    
    

def getDate():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time
def getFact():
    rfact = [randfacts.getFact(),randfacts.getFact(),randfacts.getFact()]
    return rfact

class Stock:
    def __init__(self, n, c,hour, day):
        self.name = n
        self.current = c
        self.last1 = hour
        self.last24 = day

@app.route("/api/stock")
def apiStock():
    #symbol = 'DOGE'
    #symbol = 'LTC'
    #symbol = 'SHIB'
    #symbol = 'XRP'
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'convert': 'EUR',
        'symbol': symbol
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '707ecde0-df8f-46e8-8d80-dca81c365419',
    }

    session = Session()
    session.headers.update(headers)

    try:
        CryptoList = []
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        for crypto in data["data"]:

            _name = data["data"][symbol]["name"]
            _price = data["data"][symbol]["quote"]["EUR"]["price"]
            _perchange1 = data["data"][symbol]["quote"]["EUR"]["percent_change_1h"]
            _perchange24 = data["data"][symbol]["quote"]["EUR"]["percent_change_24h"]
            
            #cryptoData = {'name': _name, 'price': _price, 'perchange': _perchange}

            #CryptoList.append(Stock(_name,_price, _perchange1, _perchange24));
            return jsonify({"current":_price, "last1": _perchange1, "last24": _perchange24});
            
        #return json.dumps(CryptoList[0])
        return CryptoList[0]
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def getStock():
    #symbol = 'DOGE'
    #symbol = 'LTC'
    symbol = 'SHIB'
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'convert': 'EUR',
        'symbol': symbol
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '707ecde0-df8f-46e8-8d80-dca81c365419',
    }

    session = Session()
    session.headers.update(headers)

    try:
        CryptoList = []
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        for crypto in data["data"]:

            _name = data["data"][symbol]["name"]
            _price = data["data"][symbol]["quote"]["EUR"]["price"]
            _perchange1 = data["data"][symbol]["quote"]["EUR"]["percent_change_1h"]
            _perchange24 = data["data"][symbol]["quote"]["EUR"]["percent_change_24h"]
            
            #cryptoData = {'name': _name, 'price': _price, 'perchange': _perchange}

            CryptoList.append(Stock(_name,_price, _perchange1, _perchange24));

        #return json.dumps(CryptoList[0])
        return CryptoList[0]
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

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
    def __init__(self, t, c, u, cat):
        self.title = t
        self.content = c
        self.url = u
        self.category = cat
def getNews():
    
    newsapi = NewsApiClient(api_key='94454bdacf3247a2957f23c8de7f597f')

    ########  Irish Headlines
        # Top Irish headlines
    irish_headlines = newsapi.get_top_headlines(country='ie')
    irishList = []
    for items in irish_headlines:
        if(items == 'articles'):
            for articles in irish_headlines[items]:                
                irishList.append ( NewsStory(articles['title'],articles['content'], articles['url'], 'Irish'))  


    ########  All Headlines
                # All Tech headlines
    headlines = newsapi.get_top_headlines()
    techList = []
    for items in headlines:
         if(items == 'articles'):
             for articles in headlines[items]:                
                 irishList.append( NewsStory(articles['title'],articles['content'], articles['url'], 'All'))
                 
    crypto_headlines = newsapi.get_top_headlines(category='business', language='en')
    cryptoList = []
    for items in crypto_headlines:
         if(items == 'articles'):
             for articles in crypto_headlines[items]:                
                 cryptoList.append( NewsStory(articles['title'],articles['content'], articles['url'], 'Crypto'))
                 
    return techList , irishList, cryptoList

@app.route('/getNewsSearch', methods=['POST'])
def searchNews():
    newsapi = NewsApiClient(api_key='94454bdacf3247a2957f23c8de7f597f')
    
    searchItems = newsapi.get_everything(q='sligo',language='en', sort_by='relevancy')
    searchnewsstr = ""
    searchnewsList = []
    
    for items in searchItems:
        if(items =='articles'):
            for articles in searchItems[items]:
                story = NewsStory(articles['title'],articles['content'],'Search')
                jsonstory = json.dumps(story.__dict__)
                searchnewsList += jsonstory
                searchnewsList.append(jsonstory)
                
    #loadPage(searchnewsList)
    #return render_template("index.html", newsstr = getNews(), fact = getFact(), searchnews = searchnewsList, newscount = 0, word = getWord())
    #return render_template('index.html', newsList = searchnewsList)
    #jsonList = json.dumps(searchnewsList)
    return json.dumps({'newslist': searchnewsList})

class Country:
    def __init__(self, t, sr, url, cap ,pop , tz, latlng):
        self.title = t
        self.subregion = sr
        self.flagurl = url
        self.capital = cap
        self.population = pop
        self.timezone = tz
        self.latlng = latlng
        

def getCountry():
    response = requests.get("https://restcountries.eu/rest/v2/all", json={'key':'value'})
    response = response.json()
    countries = []
    countryitems = []
    for items in response:
        countries.append(Country(items['name'], items['subregion'],items['flag'], items['capital'], items['population'] , items['timezones'], items['latlng']))
        testcountry = items['name']
        
        
    country = (countries[random.randint(0,len(countries))])
    #countryitems.append(country.name)
    return country


if __name__ == "__main__":
    app.run()