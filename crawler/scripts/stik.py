from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json


def get_stik(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tspan"))
        )
    except Exception as e:
        pass


    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    statistics = {}

    possession_title = soup.find("div", class_="unterueberschrift", string=lambda s: s and "Possession" in s)
    if possession_title:
        possession_container = possession_title.find_next_sibling("div", class_="sb-st-ballbesitz")
        if possession_container:
            home_a = possession_container.find("a", class_="sb-st-wappen-heim")
            away_a = possession_container.find("a", class_="sb-st-wappen-gast")
            home_team = home_a.get("title", "").strip() if home_a else ""
            away_team = away_a.get("title", "").strip() if away_a else ""
            data_labels = possession_container.find_all("tspan")
            if len(data_labels) >= 2:
                home_value = data_labels[2].get_text(strip=True)
                away_value = data_labels[1].get_text(strip=True)
            else:
                home_value = away_value = None

            statistics["possession"] = {
                "home": {"team": home_team, "value": home_value},
                "away": {"team": away_team, "value": away_value}
            }

    for category_div in soup.find_all("div", class_="unterueberschrift"):
        category_text = category_div.get_text(strip=True)
        if "Possession" in category_text:
            continue
        category_key = category_text.lower().replace(" ", "_")

        stat_container = category_div.find_next_sibling("div", class_="sb-statistik")
        if stat_container:
            lis = stat_container.find_all("li")
            if len(lis) >= 2:
                home_li = lis[0]
                away_li = lis[1]
                home_value = home_li.find("div", class_="sb-statistik-zahl").get_text(strip=True) if home_li.find("div",
                                                                                                                  class_="sb-statistik-zahl") else None
                away_value = away_li.find("div", class_="sb-statistik-zahl").get_text(strip=True) if away_li.find("div",
                                                                                                                  class_="sb-statistik-zahl") else None

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

    output = {"statistics": statistics}
    return output