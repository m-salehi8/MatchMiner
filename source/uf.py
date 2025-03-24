import json
from bs4 import BeautifulSoup
import requests
from requests import session

from source.utils import get_random_user_agent
from source.models import LeagueLinks, Source, MatchLinks, LeagueSeasonLinks
from urllib.parse import urlparse, parse_qs


def get_query_params(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params



def get_games(session):
    print("Start  ======>>>>>>>>    ", session)
    headers = {"User-Agent": get_random_user_agent()}
    response = requests.get(session.url, headers=headers)
    if response.status_code != 200:
        print(response.status_code)
        print('sssssssssssss')
        return False

    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    boxes = soup.find_all("div", class_="box")
    for box in boxes:
        table = box.find("table")
        body = table.find("tbody")
        a = body.find_all('a')
        a = list(reversed(a))
        for h in a:
            url = h.get("href")
            if "index" in url :
                n = "https://www.transfermarkt.com" + url
                url_split = n.split('/')
                title = url_split[3]
                mid = url_split[-1]

                # if not match:
                match = MatchLinks()

                match.session = session
                match.match_id = mid
                match.title = title
                match.url =  n
                match.status = "in_queue"
                match.save()
                print("Saved  =====>>>>>>>      ", title, )


def generate_urls(url_template, start_year, end_year):

    return [url_template.format(year) for year in range(start_year, end_year + 1)]


def con(session):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    res = requests.get(
        session.url,
        headers=HEADERS)
    if res.status_code != 200:
        return None

    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("div", class_="large-8 columns")
    box = table.find("div", class_="box pokalWettbewerbSpieltagsbox")
    matches = box.find_all("tr", class_="begegnungZeile")
    m = []
    for match in matches:
        tds = match.find_all("td")
        for i, td in enumerate(tds):
            if td.text:
                print(i, "   =======   ", td.text.strip())

        home_team = tds[3].text.strip()

        result = tds[4]
        match_link = result.find("a")
        if match_link:
            match_link = match_link.get("href")
        match_result = result.text.strip()
        away_team = tds[5].text.strip()
        n = "https://www.transfermarkt.com" + match_link
        url_split = n.split('/')
        title = f"{home_team.replace(' ', '-' )}_{away_team.replace(' ', '-')}"
        mid = url_split[-1]

        match = MatchLinks()
        match.session = session
        match.match_id = mid
        match.title = title
        match.url = n
        match.status = "in_queue"
        match.save()

        print(match_link)
        print(home_team.strip())
        print(away_team.strip())
        print("*****************************************************")



def run(league):
    urls = generate_urls(league.url, league.start_year, league.end_year)
    urls = list(reversed(urls))
    for url in urls:
        params = get_query_params(url)
        year = params.get("saison_id", None)[0]
        match_count = params.get("spieltagBis", [0, ])[0]
        session = LeagueSeasonLinks.objects.filter(league=league, year=year, url=url).first()
        if not session:
            session = LeagueSeasonLinks()

            session.url= url
            session.league = league
            session.year =year
            session.match_count = match_count
            session.save()

        match_urls = con(session)



source = Source.objects.all().first()
leagues = LeagueLinks.objects.filter(source=source, name="UEFA Europa League Qualifying")
for league in leagues:
    if league.url:
        run(league)
#
#


