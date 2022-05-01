import requests
from bs4 import BeautifulSoup as bs
from tinydb import TinyDB


db = TinyDB('TV_shows.json')
url = "https://www.imdb.com/chart/tvmeter/?ref_=nv_tvv_mptv"
r = requests.get(url)
soup = bs(r.text, 'lxml')

results = []
shows = soup.select("tbody tr")
for show in shows:
    link_ = show.select_one("td.posterColumn a")['href']
    link = f"https://www.imdb.com{link_}"
    name = show.select_one('td.posterColumn a').img['alt']
    rank = show.select_one("td.posterColumn span:nth-child(1)")['data-value']
    rating = show.select_one("td.posterColumn span:nth-child(2)")['data-value']
    year = show.select_one('td:nth-child(2) span.secondaryInfo').text[1:-1]

    result = {
        'rank': rank,
        'name': name,
        'year': year,
        'rating': rating,
        'link': link
    }
    results.append(result)
    db.insert(result)