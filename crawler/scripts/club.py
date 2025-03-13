import os
import re
import json
import requests
from bs4 import BeautifulSoup

def get_data_club(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    result = {}
    facts_section = soup.find("div", class_="box daten-und-fakten")
    facts_data = {}
    if facts_section:
        header = facts_section.find("h2", class_="content-box-headline")
        facts_data["header"] = header.get_text(strip=True) if header else ""

        table_elem = facts_section.find("table")
        teams = {}
        if table_elem:
            thead = table_elem.find("thead")
            if thead:
                left_div = thead.find("td", class_="table-head-zwei-links")
                right_div = thead.find("td", class_="table-head-zwei-rechts")
                if left_div:
                    name_div = left_div.find("div", class_="vereinsname")
                    teams["left"] = name_div.get_text(strip=True) if name_div else ""
                if right_div:
                    name_div = right_div.find("div", class_="vereinsname")
                    teams["right"] = name_div.get_text(strip=True) if name_div else ""
            facts_data["teams"] = teams

            facts = {}
            tbody = table_elem.find("tbody")
            if tbody:
                rows = tbody.find_all("tr")
                current_category = None
                for row in rows:
                    cat_td = row.find("td", class_="daten-und-fakten-kategorie")
                    if cat_td:
                        current_category = cat_td.get_text(strip=True)
                    else:
                        tds = row.find_all("td")
                        if len(tds) == 2 and current_category:
                            def parse_td(td):
                                span = td.find("span", class_="datenundfakten_bar")
                                value = span.get_text(strip=True) if span else td.get_text(strip=True)
                                style = span.get("style", "") if span else ""
                                width_match = re.search(r'width:\s*([\d\.]+)%', style)
                                width = width_match.group(1) if width_match else None
                                if value.strip() == "?":
                                    value = None
                                return {"value": value, "width": width}

                            left_data = parse_td(tds[0])
                            right_data = parse_td(tds[1])
                            facts[current_category] = {"left": left_data, "right": right_data}
            facts_data["facts"] = facts
    result["facts_and_figures"] = facts_data

    # استخراج "Last 10 meetings"
    meetings_data = []
    h2_meetings = soup.find("h2", class_="content-box-headline", string=lambda s: s and "Last 10 meetings" in s)
    if h2_meetings:
        meetings_box = h2_meetings.find_parent("div", class_="box")
        table = meetings_box.find("table")
        if table:
            tbody = table.find("tbody")
            if tbody:
                for row in tbody.find_all("tr"):
                    cells = row.find_all("td")
                    if len(cells) >= 9:
                        meeting = {}
                        comp_img = cells[0].find("img")
                        meeting["competition_logo"] = comp_img["src"] if comp_img and comp_img.has_attr("src") else None
                        meeting["competition"] = comp_img["alt"] if comp_img and comp_img.has_attr("alt") else None
                        meeting["matchday"] = cells[1].get_text(strip=True)
                        meeting["date"] = cells[2].get_text(strip=True)
                        # Home team
                        home_img = cells[3].find("img")
                        meeting["home_team_logo"] = home_img["src"] if home_img and home_img.has_attr("src") else None
                        home_text = cells[4].get_text(" ", strip=True)
                        match_home = re.match(r'(.+?)\s*\((.*?)\)', home_text)
                        if match_home:
                            meeting["home_team"] = match_home.group(1).strip()
                            meeting["home_team_rank"] = match_home.group(2).strip()
                        else:
                            meeting["home_team"] = home_text
                            meeting["home_team_rank"] = None
                        # Away team
                        away_img = cells[5].find("img")
                        meeting["away_team_logo"] = away_img["src"] if away_img and away_img.has_attr("src") else None
                        away_text = cells[6].get_text(" ", strip=True)
                        match_away = re.match(r'(.+?)\s*\((.*?)\)', away_text)
                        if match_away:
                            meeting["away_team"] = match_away.group(1).strip()
                            meeting["away_team_rank"] = match_away.group(2).strip()
                        else:
                            meeting["away_team"] = away_text
                            meeting["away_team_rank"] = None
                        meeting["attendance"] = cells[7].get_text(strip=True)
                        result_link = cells[8].find("a")
                        meeting["result"] = result_link.get_text(strip=True) if result_link else cells[8].get_text(strip=True)
                        meeting["result_link"] = result_link["href"] if result_link and result_link.has_attr("href") else None
                        span_result = cells[8].find("span")
                        meeting["result_color"] = span_result.get("class") if span_result else None
                        meetings_data.append(meeting)
        footer_link = meetings_box.find("div", class_="table-footer").find("a")
        all_matches_link = footer_link["href"] if footer_link and footer_link.has_attr("href") else None
        result["last_10_meetings"] = {"meetings": meetings_data, "all_matches_link": all_matches_link}

    # استخراج اطلاعات مربتوط به مربیان (Coaches)
    coaches = {}
    coach_boxes = soup.find_all("div", class_="box")
    for box in coach_boxes:
        header = box.find("div", class_="spielername-profil")
        if header and "Current coach" in header.get_text():
            coach = {}
            icon = box.find("div", class_="icons-profil").find("a")
            team = icon.get("title", "").strip() if icon else ""
            coach["team"] = team
            name_elem = box.find("div", class_="container-hauptinfo")
            coach["name"] = name_elem.get_text(strip=True) if name_elem else ""
            photo = box.find("div", class_="container-foto").find("img")
            coach["image"] = photo["src"] if photo and photo.has_attr("src") else None
            additional = box.find("div", class_="container-zusatzinfo-small")
            if additional:
                lines = [line.strip() for line in additional.decode_contents().split("<br>") if line.strip()]
                clean_lines = [BeautifulSoup(line, "html.parser").get_text(" ", strip=True) for line in lines]
                coach["additional_info"] = clean_lines
            else:
                coach["additional_info"] = None
            records = []
            for tbl in box.find_all("table", class_="table-border"):
                record = {}
                title_td = tbl.find("td", class_="hauptlink bg_ueberschrift")
                record["record_title"] = title_td.get_text(strip=True) if title_td else ""
                rows = tbl.find_all("tr")
                if len(rows) >= 3:
                    headers = [th.get_text(strip=True) for th in rows[1].find_all("td")]
                    data = [td.get_text(strip=True) for td in rows[2].find_all("td")]
                    record["data"] = dict(zip(headers, data)) if len(headers) == len(data) else data
                records.append(record)
            coach["records"] = records
            coaches[team] = coach
    result["current_coaches"] = coaches

    # استخراج انتقالات بین باشگاه‌ها (Transfers between each other)
    transfers = []
    top_transfers_box = None
    h2_transfers = soup.find("h2", class_="content-box-headline",
                             string=lambda s: s and "Transfers between each other" in s)
    if h2_transfers:
        top_transfers_box = h2_transfers.find_parent("div", class_="box")
    if top_transfers_box:
        table = top_transfers_box.find("table")
        if table:
            tbody = table.find("tbody")
            if tbody:
                for row in tbody.find_all("tr"):
                    tds = row.find_all("td")
                    if len(tds) < 9:
                        continue
                    transfer = {}
                    transfer["season"] = tds[0].get_text(strip=True)
                    player_cell = tds[1]
                    player_table = player_cell.find("table", class_="inline-table")
                    player = {}
                    if player_table:
                        p_rows = player_table.find_all("tr")
                        if p_rows:
                            first_row = p_rows[0]
                            p_cells = first_row.find_all("td")
                            if len(p_cells) >= 2:
                                img = p_cells[0].find("img")
                                player["image"] = img["src"] if img and img.has_attr("src") else None
                                a_tag = p_cells[1].find("a")
                                player["name"] = a_tag.get_text(strip=True) if a_tag else ""
                                player["profile_url"] = a_tag["href"] if a_tag and a_tag.has_attr("href") else ""
                        if len(p_rows) > 1:
                            second_row = p_rows[1]
                            player["position"] = second_row.get_text(strip=True)
                    transfer["player"] = player
                    nat_cell = tds[2]
                    flags = nat_cell.find_all("img")
                    transfer["nationality"] = [img["alt"] for img in flags if img.has_attr("alt")]
                    left_cell = tds[3]
                    left_table = left_cell.find("table", class_="inline-table")
                    left_team = {}
                    if left_table:
                        l_rows = left_table.find_all("tr")
                        if l_rows:
                            first_row = l_rows[0]
                            l_cells = first_row.find_all("td")
                            if l_cells:
                                a_tag = l_cells[0].find("a")
                                left_team["logo"] = a_tag.find("img")["src"] if a_tag and a_tag.find("img") and a_tag.find("img").has_attr("src") else None
                            if len(l_cells) >= 2:
                                left_team["name"] = l_cells[1].get_text(strip=True)
                        if len(l_rows) > 1:
                            second_row = l_rows[1]
                            left_team["additional"] = second_row.get_text(strip=True)
                    transfer["left_team"] = left_team
                    joined_cell = tds[4]
                    joined_table = joined_cell.find("table", class_="inline-table")
                    joined_team = {}
                    if joined_table:
                        j_rows = joined_table.find_all("tr")
                        if j_rows:
                            first_row = j_rows[0]
                            j_cells = first_row.find_all("td")
                            if j_cells:
                                a_tag = j_cells[0].find("a")
                                joined_team["logo"] = a_tag.find("img")["src"] if a_tag and a_tag.find("img") and a_tag.find("img").has_attr("src") else None
                            if len(j_cells) >= 2:
                                joined_team["name"] = j_cells[1].get_text(strip=True)
                        if len(j_rows) > 1:
                            second_row = j_rows[1]
                            joined_team["additional"] = second_row.get_text(strip=True)
                    transfer["joined_team"] = joined_team
                    transfer["transfer_date"] = tds[5].get_text(strip=True)
                    transfer["fee"] = tds[6].get_text(strip=True)
                    transfers.append(transfer)
    result["transfers_between_each_other"] = transfers

    # استخراج جدول Premier League
    table_box = None
    h2_table = soup.find("h2", class_="content-box-headline", string=lambda s: s and "Table Premier League" in s)
    if h2_table:
        table_box = h2_table.find_parent("div", class_="box")
    table_data = {}
    if table_box:
        header = table_box.find("h2", class_="content-box-headline")
        table_data["header"] = header.get_text(strip=True) if header else ""
        table_elem = table_box.find("table")
        if table_elem:
            thead = table_elem.find("thead")
            if thead:
                table_data["headers"] = [th.get_text(strip=True) for th in thead.find_all("th")]
            tbody = table_elem.find("tbody")
            rows = []
            if tbody:
                for row in tbody.find_all("tr"):
                    cells = [cell.get_text(strip=True) for cell in row.find_all("td")]
                    rows.append(cells)
                table_data["rows"] = rows
    result["table_premier_league"] = table_data

    # استخراج Overall balance Premier League
    overall_box = None
    h2_overall = soup.find("h2", class_="content-box-headline",
                           string=lambda s: s and "Overall balance Premier League" in s)
    if h2_overall:
        overall_box = h2_overall.find_parent(lambda tag: tag.name in ["div", "section"] and "box" in tag.get("class", []))
    overall_balance = {}
    if overall_box:
        header = overall_box.find("h2", class_="content-box-headline")
        overall_balance["header"] = header.get_text(strip=True) if header else ""
        rows_data = []
        rows = overall_box.find_all("div", class_="balance-sheet__row")
        for row in rows:
            cols = row.find_all("span")
            if len(cols) >= 4:
                row_dict = {
                    "label": cols[0].get_text(strip=True),
                    "team_icon": cols[1].find("img")["src"] if cols[1].find("img") and cols[1].find("img").has_attr("src") else cols[1].get_text(strip=True),
                    "team": cols[2].get_text(strip=True),
                    "value": cols[3].get_text(strip=True)
                }
                rows_data.append(row_dict)
        overall_balance["rows"] = rows_data
    result["overall_balance_premier_league"] = overall_balance

    # استخراج Most valuable players
    mvps = {}
    mvp_boxes = soup.find_all("div", class_="box vereinsvergleich-singlespieler")
    for box in mvp_boxes:
        header = box.find("div", class_="spielername-profil")
        if header and "Most valuable player" in header.get_text():
            mvp = {}
            icon = box.find("div", class_="icons-profil").find("a")
            team = icon.get("title", "").strip() if icon else ""
            mvp["team"] = team
            foto = box.find("div", class_="headervergleichfoto").find("img")
            mvp["image"] = foto["src"] if foto and foto.has_attr("src") else None
            profile_table = box.find("table", class_="profilheader")
            profile = {}
            if profile_table:
                for row in profile_table.find_all("tr"):
                    th = row.find("th")
                    td = row.find("td")
                    if th and td:
                        key = th.get_text(strip=True).replace(":", "")
                        value = td.get_text(" ", strip=True)
                        profile[key] = value
            mvp["profile"] = profile
            cmv = box.find("div", class_="aktueller-marktwert")
            if cmv:
                value = cmv.get_text(strip=True)
                value = re.sub(r'^Current market value:\s*', '', value)
                mvp["current_market_value"] = value
            else:
                mvp["current_market_value"] = None
            mvps[team] = mvp
    result["most_valuable_players"] = mvps

    # استخراج Transfer income/expenditure
    transfer_data = {}
    h2_transfer = soup.find("h2", class_="content-box-headline", string=lambda s: s and "Transfer income/expenditure" in s)
    if h2_transfer:
        transfer_box = h2_transfer.find_parent("div", class_="box")
        if transfer_box:
            svg = transfer_box.find("svg")
            if svg:
                title_elem = svg.find("text", class_="highcharts-title")
                if title_elem:
                    transfer_data["chart_title"] = title_elem.get_text(strip=True)
            legends = []
            for legend_item in transfer_box.find_all("g", class_="highcharts-legend-item"):
                legend = {}
                text_elem = legend_item.find("text")
                rect_elem = legend_item.find("rect")
                if text_elem:
                    legend["text"] = text_elem.get_text(strip=True)
                if rect_elem:
                    legend["color"] = rect_elem.get("fill")
                legends.append(legend)
            transfer_data["legend"] = legends
    result["transfer_income_expenditure"] = transfer_data

    # استخراج Top fixture-goal scorers
    top_scorers = {}
    h2_top = soup.find("h2", class_="content-box-headline", string=re.compile("Top fixture-goal scorers", re.I))
    if h2_top:
        top_box = h2_top.find_parent("div", class_="box")
        if top_box:
            header = top_box.find("h2", class_="content-box-headline")
            top_scorers["header"] = header.get_text(strip=True) if header else ""
            table = top_box.find("table")
            if table:
                thead = table.find("thead")
                if thead:
                    top_scorers["headers"] = [th.get_text(strip=True) for th in thead.find_all("th")]
                tbody = table.find("tbody")
                rows = []
                if tbody:
                    for row in tbody.find_all("tr"):
                        cells = [cell.get_text(strip=True) for cell in row.find_all("td")]
                        rows.append(cells)
                    top_scorers["rows"] = rows
    result["top_fixture_goal_scorers"] = top_scorers

    return result


