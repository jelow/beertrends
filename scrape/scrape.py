from bs4 import BeautifulSoup
import requests, re, collections, time, json

urls = ["https://www.beeradvocate.com/place/list/?&c_id=CA&s_id=BC&brewery=Y&sort=name&sort=numbeers",
        "https://www.beeradvocate.com/place/list/?start=20&c_id=CA&s_id=BC&brewery=Y&sort=name&sort=numbeers",
        "https://www.beeradvocate.com/place/list/?start=40&c_id=CA&s_id=BC&brewery=Y&sort=name&sort=numbeers",
        "https://www.beeradvocate.com/place/list/?start=60&c_id=CA&s_id=BC&brewery=Y&sort=name&sort=numbeers",
        ]

ratings = collections.defaultdict(dict)

for url in urls:
    listPage = requests.get(url)  # get the page of BC Breweries
    if listPage.status_code == 200:  # if the page doesn't load, don't parse
        listSoup = BeautifulSoup(listPage.content, 'html.parser')
        breweries = listSoup.find_all(
            href=re.compile('beer/profile'))  # each brewery in the db has an url with this string
        for brewery in breweries:
            name = brewery.find('b').text
            brewURL = "http://www.beeradvocate.com" + brewery['href']
            ratings[name].update({'URL': brewURL})

for breweryName, breweryURL in dict(ratings).items():  # now iterate through the individual breweries
    time.sleep(1)
    breweryPage = requests.get(breweryURL['URL'])
    if breweryPage.status_code == 200:
        brewerySoup = BeautifulSoup(breweryPage.content, 'html.parser')
        beers = brewerySoup.find_all(href=re.compile('beer/profile/(.*?[0-9])/(.*?[0-9])/'))
        for beer in beers:
            time.sleep(1)
            beerName = beer.find('b').text
            beerURL = "http://www.beeradvocate.com" + beer['href']
            ratings[breweryName].update({beerName: {'URL': beerURL}})

            # drilling down further into the individual beer pages now from each brewery
            beerRatingPage = requests.get(beerURL)
            if beerRatingPage.status_code == 200:
                beerRatingSoup = BeautifulSoup(beerRatingPage.content, 'html.parser')
                beerRatings = beerRatingSoup.find_all('div', id='rating_fullview_container')
                for rating in beerRatings:
                    time.sleep(1)
                    ratingValue = rating.text[:4]  # this is not ideal, sometimes it will pull in '4/5 ' or '4.73'
                    # depending on the rating. At this point I'm just trying to get this working...something to revisit
                    ratingDate = rating.text[-12:]  # this one actually works well
                    # "Hold on to your butts" - Sam Jack
                    ratings[breweryName][beerName].update({ratingDate: ratingValue})

with open('BAratings.json', 'w') as bar:
    json.dump(ratings, bar, sort_keys=True, indent=4)
