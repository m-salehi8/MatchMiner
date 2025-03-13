import requests
from bs4 import BeautifulSoup
import re
import time
import json
from collections import defaultdict

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

main_url = "https://www.transfermarkt.com/spielbericht/index/spielbericht/4362781"
base_url = "https://www.transfermarkt.com"



def get_main_page_soup(main_url, headers):
    response = requests.get(main_url, headers=headers)
    if response.status_code != 200:
        raise Exception("خطا در دریافت صفحه اصلی: " + str(response.status_code))
    return BeautifulSoup(response.text, "html.parser")


def extract_timeline_section(soup):
    timeline_section = soup.find("div", id="sb-zeitleiste")
    if not timeline_section:
        raise Exception("بخش تایملاین پیدا نشد.")
    return timeline_section


def extract_main_events(container, team):

    events = []

    if container:
        for event in container.find_all("div", class_="sb-leiste-ereignis"):
            style = event.get("style", "")
            left_match = re.search(r"left:\s*([\d\.]+)%", style)
            left_percentage = left_match.group(1) if left_match else None
            data_content = event.get("data-content")
            inner_span = event.find("span")
            event_type = None
            if inner_span:
                for cls in inner_span.get("class", []):
                    if cls in ["sb-tor", "sb-eigentor", "sb-rot", "sb-wechsel", "sb-gelb"]:
                        event_type = cls
                        break
            events.append({
                "team": team,
                "left_percentage": left_percentage,
                "detail_url": data_content,
                "event_type": event_type
            })
    return events


def parse_event_time(time_str):
    time_str = time_str.strip()
    numbers = re.findall(r'\d+', time_str)
    if numbers:
        minute = int(numbers[0])
    else:
        minute = 0
    return {
        "base_minute": minute,
        "extra_minute": 0,
        "total_minute": minute,
        "formatted": f"{minute}'"
    }


def get_event_detail(detail_url, left_percentage, base_url, headers):
    full_url = base_url + detail_url
    detail_response = requests.get(full_url, headers=headers)
    if detail_response.status_code != 200:
        return None
    detail_soup = BeautifulSoup(detail_response.text, "html.parser")
    detail_div = detail_soup.find("div", class_="sb-tt-ereignis")
    if not detail_div:
        return None

    time_div = detail_div.find("div", class_="sb-tt-uhr")
    raw_time =  ""  #time_div.get_text(strip=True) if time_div else ""
    if not raw_time:
        try:
            left = float(left_percentage) if left_percentage is not None else 0
            approx = round((left / 100) * 90)
            raw_time = f"{approx}'"
        except Exception:
            raw_time = "0'"
    time_info = parse_event_time(raw_time)

    type_div = detail_div.find("div", class_="sb-tt-typ")
    event_typetext = type_div.get_text(" ", strip=True) if type_div else None

    team_div = detail_div.find("div", class_="sb-tt-verein")
    team_img = team_div.find("img") if team_div else None
    team_name = team_img.get("title") if team_img else None

    player_div = detail_div.find("div", class_="sb-tt-spieler")
    player_name = None
    if player_div:
        name_div = player_div.find("div", class_="sb-tt-spielername")
        if name_div:
            player_name = name_div.get_text(" ", strip=True)

    detail_detail = detail_div.find("div", class_="sb-tt-detail")
    event_detail_text = detail_detail.get_text(" ", strip=True) if detail_detail else None

    return {
        "raw_time": raw_time,
        "event_time": time_info["formatted"],
        "base_minute": time_info["base_minute"],
        "extra_minute": time_info["extra_minute"],
        "total_minute": time_info["total_minute"],
        "event_typetext": event_typetext,
        "team_name": team_name,
        "player_name": player_name,
        "event_detail": event_detail_text
    }


def process_events(main_url, base_url, headers, delay=1):

    soup = get_main_page_soup(main_url, headers)
    timeline_section = extract_timeline_section(soup)
    home_container = timeline_section.find("div", class_="sb-leiste-heim")
    away_container = timeline_section.find("div", class_="sb-leiste-gast")

    home_events = extract_main_events(home_container, "home")
    away_events = extract_main_events(away_container, "away")
    main_events = home_events + away_events

    for event in main_events:
        detail_url = event.get("detail_url")
        if not detail_url:
            continue
        left_percentage = event.get("left_percentage")
        event_detail = get_event_detail(detail_url, left_percentage, base_url, headers)
        if event_detail:
            event.update(event_detail)
        time.sleep(delay)
    return main_events


def group_and_sort_events(main_events):
    """
    رویدادها را به سه دسته گل‌ها، کارت‌ها/خطاها و تعویض‌ها گروه‌بندی و بر اساس کل دقیقه (total_minute) مرتب می‌کند.
    """
    grouped_events = {"goals": [], "cards": [], "substitutions": []}
    for event in main_events:

        etype = event.get("event_type")
        if etype in ["sb-tor", "sb-eigentor"]:
            grouped_events["goals"].append(event)
        elif etype in ["sb-rot", "sb-gelb"]:
            grouped_events["cards"].append(event)
        elif etype == "sb-wechsel":
            grouped_events["substitutions"].append(event)
    for key in grouped_events:
        grouped_events[key] = sorted(grouped_events[key], key=lambda x: x.get("total_minute", 0))
    return grouped_events



def get_time(url):
    main_events = process_events(url, base_url, headers, delay=1)
    grouped_events = group_and_sort_events(main_events)
    return grouped_events




