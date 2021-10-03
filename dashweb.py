from flask import Flask, render_template,jsonify
from datetime import datetime
from idna import unicode
from newsapi import NewsApiClient
import json
import randfacts
import tmdbsimple as tmdb
import requests
#from random_word import RandomWords
import random
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    
    _golfLeader = False
    _golfSchedule = False
    _coun = False
    _tvguide = True
    _time = False
    _newstr = True
    _newsCount = False
    
    
    if _golfLeader == True:
        _golfLeader = getGolfLeaderboard()
        _golfSchedule = getGolfSchedule()
    if _tvguide == True:
        _tvguide = getTVGuide()
        
    #loadPage('')
    #stock = getStock()
    #golfLeader = getGolfLeaderboard(),golfSchedule = getGolfSchedule(),
    return render_template("index.html", coun = getCountry(),tvguide = _tvguide, time = getDate(),golfLeader = _golfLeader,golfSchedule = _golfSchedule, newsstr = getNews(),  fact = getFact(), newscount = 0)

def getGolfLeaderboard():
    url = "https://golf-leaderboard-data.p.rapidapi.com/tour-rankings/2/2021"

    headers = {
        'x-rapidapi-key': "6e6c8988edmsh9dde74a11f1bfa3p18e7b1jsnab2498895645",
        'x-rapidapi-host': "golf-leaderboard-data.p.rapidapi.com"
        }

    #response2 = requests.request("GET", url2, headers=headers)

    request = requests.get(url, headers=headers)
    dict = request.json()
    count = 0
    leaderboard = []
    leaders = ''

    dict1= dict.get('results')   
    for i in dict1.get('rankings'):
        if count < 10:
            name = i['player_name']
            position = i['position']
            leaderboard.append(name)
            leaders += 'Position '+str(position)+':\n'+name+'\n' 
            count += 1 
        else:
            break
     
            

    return leaderboard   #for raspberry pi
    #print (leaders)       # for laptop


def getGolfSchedule():
    import datetime
    upcoming = ''
    upcoming_list = []
    now = datetime.datetime.now()
    count = 0


    url = "https://golf-leaderboard-data.p.rapidapi.com/fixtures/2/2021"

    headers = {
        'x-rapidapi-key': "6e6c8988edmsh9dde74a11f1bfa3p18e7b1jsnab2498895645",
        'x-rapidapi-host': "golf-leaderboard-data.p.rapidapi.com"
        }



    request = requests.get(url, headers=headers)
    json = request.json()
    #json = list(json)

    for i in json.get('results'):
        if count >= 3:
            break
        name = i["name"]
        course = i["course"]
        country = i["country"]
        starting = i["start_date"]
        ending = i["end_date"]
        prize = i["prize_fund"]
        datecheck = [now.year, now.month, now.day] 
        datecheck2 = starting.split(' ')
        datecheck2.pop(1)
        datecheck2 = datecheck2[0].split('-')
        starting1 = datetime.datetime(int(datecheck2[0]), int(datecheck2[1]), int(datecheck2[2]))
        now1 = datetime.datetime(int(datecheck[0]), int(datecheck[1]), int(datecheck[2]))
        comp = 1
       
        if starting1 < now1:
            continue
          
        else:
            upcoming += 'Upcoming Golf Tournaments\n' 'Name: '+name+ '\nCountry: '+country+ '\nStarting on: '+starting+ '\nPrize money: '+prize+'\n'
            upcoming_list.append(name)
        count += 1 

    #print (upcoming)        #for laoptop
    return upcoming_list   #for raspberry pi


def getTVGuide():
    pages = ['&page=1','&page=2', '&page=3', '&page=4', '&page=5']
    upcoming = []
    thisweek = ''
    favourites = ['Rick & Morty', 'Superman & Lois', 'Greys Anatomy', 'Legacies', 'Loki', "DC's legends of tomorrow", 'The Flash', 'Clarksons Farm', "America's Got Talent", 'The voice']


    for items in pages:

        url2 = "https://api.themoviedb.org/3/tv/on_the_air?api_key=74d5287b6bd749f76603010fdcf24585&language=en-US"+str(items)
     
        request2 = requests.get(url2)
        dict = request2.json()
        
        for i in dict.get('results'):
            y = i["name"]
            if y in favourites:
                upcoming.append(y)
                thisweek += y +'\n'

    
    return upcoming
        
        
        
    

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