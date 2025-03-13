from bs4 import BeautifulSoup
import json
import requests

def get_data_stik(url, output_file):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    req = requests.get(url, headers=headers)
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')
    statistics = {}

    possession_title = soup.find("div", class_="unterueberschrift", string=lambda s: s and "Possession" in s)
    if possession_title:
        possession_container = possession_title.find_next_sibling("div", class_="sb-st-ballbesitz")
        if possession_container:
            home_a = possession_container.find("a", class_="sb-st-wappen-heim")
            away_a = possession_container.find("a", class_="sb-st-wappen-gast")
            home_team = home_a.get("title", "").strip() if home_a else ""
            away_team = away_a.get("title", "").strip() if away_a else ""
            possession_labels = possession_container.select(".highcharts-data-labels tspan")
            if len(possession_labels) >= 2:
                away_value = possession_labels[0].get_text(strip=True)
                home_value = possession_labels[1].get_text(strip=True)
            else:
                home_value = away_value = None

            statistics["possession"] = {
                "home": {"team": home_team, "value": home_value},
                "away": {"team": away_team, "value": away_value}
            }

    # استخراج سایر آمار (مانند Total shots، Shots off target، …)
    for category_div in soup.find_all("div", class_="unterueberschrift"):
        category_text = category_div.get_text(strip=True)
        if "Possession" in category_text:
            continue  # از پردازش دوباره Possession صرفنظر می‌کنیم
        category_key = category_text.lower().replace(" ", "_")
        stat_container = category_div.find_next_sibling("div", class_="sb-statistik")
        if stat_container:
            lis = stat_container.find_all("li")
            if len(lis) >= 2:
                home_li = lis[0]
                away_li = lis[1]
                home_value_tag = home_li.find("div", class_="sb-statistik-zahl")
                away_value_tag = away_li.find("div", class_="sb-statistik-zahl")
                home_value = home_value_tag.get_text(strip=True) if home_value_tag else None
                away_value = away_value_tag.get_text(strip=True) if away_value_tag else None

                home_team = ""
                away_team = ""
                home_wappen = home_li.find("div", class_="sb-statistik-wappen")
                away_wappen = away_li.find("div", class_="sb-statistik-wappen")
                if home_wappen:
                    a_tag = home_wappen.find("a")
                    if a_tag:
                        home_team = a_tag.get("title", "").strip()
                if away_wappen:
                    a_tag = away_wappen.find("a")
                    if a_tag:
                        away_team = a_tag.get("title", "").strip()

                statistics[category_key] = {
                    "home": {"team": home_team, "value": home_value},
                    "away": {"team": away_team, "value": away_value}
                }

#    output = {f"data/stik/{output_file}.json": statistics}
#    with open(output_file, "w", encoding="utf-8") as outfile:
#        json.dump(output, outfile, indent=2, ensure_ascii=False)

    with open(f"{output_file}.json", "w", encoding="utf-8") as f:
        j = json.dumps(statistics, ensure_ascii=False, indent=4)
        f.write(j)


url = "https://www.transfermarkt.com/arsenal-fc_everton-fc/statistik/spielbericht/4095452"
get_data_stik(url, "data")
