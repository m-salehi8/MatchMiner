from bs4 import BeautifulSoup
import json
import re
import  requests


def get_data_line(url):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    html = requests.get(url, headers=HEADERS).text

    soup = BeautifulSoup(html, "html.parser")
    teams_data = {}

    blocks = soup.find_all("div", class_="large-6 columns")
    for block in blocks:
        header = block.find("h2")
        if not header:
            continue
        a_tag = header.find("a")
        if not a_tag:
            continue
        team_name = a_tag.get("title", "").strip()
        header_text = header.get_text(" ", strip=True)

        if "Starting Line-up" in header_text:
            block_type = "starting_lineup"
        elif "Substitutes" in header_text:
            block_type = "substitutes"
        elif "Manager" in header_text:
            block_type = "manager"
        else:
            block_type = header_text.lower().replace(" ", "_")

        if team_name not in teams_data:
            teams_data[team_name] = {"name": team_name}

        if block_type in ["starting_lineup", "substitutes"]:
            players = []
            table = block.find("table", class_="items")
            if table:
                rows = table.find_all("tr", recursive=False)
                for row in rows:
                    tds = row.find_all("td", recursive=False)
                    if len(tds) < 3:
                        continue

                    number_div = tds[0].find("div", class_="rn_nummer")
                    number = number_div.get_text(strip=True) if number_div else None

                    nested_table = tds[1].find("table", class_="inline-table")
                    if nested_table:
                        nested_rows = nested_table.find_all("tr")
                        first_row_tds = nested_rows[0].find_all("td", recursive=False)
                        if len(first_row_tds) >= 2:
                            a_profile = first_row_tds[0].find("a")
                            player_profile_url = a_profile["href"] if a_profile and a_profile.has_attr("href") else None
                            img_tag = a_profile.find("img") if a_profile else None
                            image_url = img_tag["src"] if img_tag and img_tag.has_attr("src") else None

                            a_name = first_row_tds[1].find("a")
                            name = a_name.get_text(strip=True) if a_name else None
                            captain = bool(first_row_tds[1].find("span", title="Team captain"))

                            age = None
                            text_info = first_row_tds[1].get_text(" ", strip=True)
                            age_match = re.search(r"\((\d+)\s+years old\)", text_info)
                            if age_match:
                                age = int(age_match.group(1))
                        else:
                            name = None
                            player_profile_url = None
                            image_url = None
                            age = None
                            captain = False

                        position = None
                        market_value = None
                        if len(nested_rows) > 1:
                            second_row_text = nested_rows[1].get_text(" ", strip=True)
                            parts = [p.strip() for p in second_row_text.split(",")]
                            if parts:
                                position = parts[0]
                            if len(parts) > 1 and parts[1]:
                                market_value = parts[1]
                        else:
                            position = None
                            market_value = None
                    else:
                        name = None
                        player_profile_url = None
                        image_url = None
                        age = None
                        captain = False
                        position = None
                        market_value = None

                    status = tds[1].get("title", "").strip() or None

                    nationality_imgs = tds[2].find_all("img")
                    nationalities = [img.get("alt", "").strip() for img in nationality_imgs if img.get("alt", "").strip()]

                    detail_url = a_name["href"] if a_name and a_name.has_attr("href") else None

                    player_data = {
                        "number": number,
                        "name": name,
                        "age": age,
                        "position": position,
                        "market_value": market_value,
                        "status": status,
                        "captain": captain,
                        "player_profile_url": player_profile_url,
                        "detail_url": detail_url,
                        "image_url": image_url,
                        "nationality": nationalities
                    }
                    players.append(player_data)

            statistics = {}
            footer = block.find("div", class_="table-footer")
            if footer:
                footer_tds = footer.find_all("td")
                if footer_tds and len(footer_tds) >= 4:
                    statistics["foreigners"] = footer_tds[0].get_text(strip=True)
                    statistics["avg_age"] = footer_tds[1].get_text(strip=True).replace("Avg. age: ", "")
                    statistics["purchase_value"] = footer_tds[2].get_text(strip=True).replace("Purchase value: ", "")
                    statistics["total_mv"] = footer_tds[3].get_text(strip=True).replace("Total MV: ", "")

            teams_data[team_name][block_type] = {
                "players": players,
                "statistics": statistics
            }

        elif block_type == "manager":
            table = block.find("table", class_="items")
            if table:
                row = table.find("tr")
                if row:
                    nested_table = row.find("table", class_="inline-table")
                    manager_profile_url = None
                    manager_image_url = None
                    manager_name = None
                    manager_age = None
                    if nested_table:
                        nested_rows = nested_table.find_all("tr")
                        if len(nested_rows) > 0:
                            first_row = nested_rows[0]
                            tds = first_row.find_all("td")
                            if tds:
                                a_manager = tds[0].find("a")
                                if a_manager:
                                    manager_profile_url = a_manager.get("href")
                                    img_tag = a_manager.find("img")
                                    if img_tag:
                                        manager_image_url = img_tag.get("src")
                                if len(tds) > 1:
                                    a_name = tds[1].find("a")
                                    if a_name:
                                        manager_name = a_name.get_text(strip=True)
                        if len(nested_rows) > 1:
                            second_row = nested_rows[1]
                            age_text = second_row.get_text(strip=True)
                            age_match = re.search(r"(\d+)", age_text)
                            if age_match:
                                manager_age = int(age_match.group(1))
                    tds = row.find_all("td")
                    nationalities = []
                    if tds:
                        td_nationality = tds[-1]
                        imgs = td_nationality.find_all("img")
                        for img in imgs:
                            alt = img.get("alt", "").strip()
                            if alt:
                                nationalities.append(alt)

                    manager_data = {
                        "name": manager_name,
                        "age": manager_age,
                        "player_profile_url": manager_profile_url,
                        "image_url": manager_image_url,
                        "nationality": nationalities
                    }
                    teams_data[team_name][block_type] = manager_data

    result = {"teams": list(teams_data.values())}

    return result