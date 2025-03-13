from bs4 import BeautifulSoup
from .func import get_league, get_team_data, get_match_result, get_other_match, get_lineups
import json
import requests

def crawl_data_sheet(url):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    data = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(data, 'html.parser')
    league = get_league(soup)
    team_data = get_team_data(soup)
    match_result = get_match_result(soup)
    other_match = get_other_match(soup)
    result= {
        "league": league,
        "teams": team_data,
        "match_result": match_result,
        "related_data": other_match,
    }

    return result