from bs4 import BeautifulSoup


def get_league(soup):
    head_div = soup.find('div', class_="box sb-spielbericht-head")
    league = head_div.find('div', class_="direct-headline__header-box")
    icon_tag = head_div.find('div', class_="icons-profil")
    icon = icon_tag.find('img').get('src')
    title = league.find('div', class_="spielername-profil").text.strip()
    return {
        'title': title,
        'icon': icon
    }

def get_team_data(soup):
    head_div = soup.find('div', class_="box sb-spielbericht-head")
    home_team = head_div.find('div', class_="sb-team sb-heim")
    guest_team = head_div.find('div', class_="sb-team sb-gast")

    teams = {
        'home_team': {
            "title": home_team.find('a', class_="sb-vereinslink").text.strip(),
            "icon": home_team.find('img').get('src'),
            "position": home_team.find('p').text.split('Position:')[1].strip(),
        },
        'guest_team': {
            "title": guest_team.find('a', class_="sb-vereinslink").text.strip(),
            "icon": guest_team.find('img').get('src'),
            "position": guest_team.find('p').text.split('Position:')[1].strip(),
        }
    }
    return teams


def get_match_result(soup):
    head_div = soup.find('div', class_="box sb-spielbericht-head")
    result = head_div.find('div', class_="sb-spieldaten")
    small_title = result.find('p').text.split('|')
    small_title = [st.strip() for st in small_title]

    r = result.find('div', class_="sb-endstand").text.split('(')
    overtime = r[0].strip()
    end_result = r[1].strip()[:-1]


    sub_data = result.find('p', class_='sb-zusatzinfos')
    stadium = sub_data.find_all('a')
    stadium = {
        'name': stadium[0].text,
        'url': stadium[0].get('href'),
        'referee': stadium[1].get('title'),
        'referee_url': stadium[1].get('href')
    }
    attendance = sub_data.find('strong').text
    return {
        'date': small_title,
        'match_result': overtime,
        'end_result': end_result,
        'attendance': attendance,
        'stadium': stadium

    }


def get_other_match(soup):
    # head_div = soup.find('div', class_="box sb-spielbericht-head")
    match_tag = soup.find('div', class_='clearer footer sb-begegnungsliste-small-link')
    match_list = match_tag.find_all('td')
    res_match_list = []
    for ma in match_list:
        teams = ma.find_all('img' )
        result = ma.find('span').text
        res_match_list.append({
            'home_team': {
                'title': teams[0].get('title'),
                'icon': teams[0].get('src'),
            },
            'guest_team': {
                "title": teams[1].get('title'),
                "icon": teams[1].get('src')
            },
            "result": result

        })

    return res_match_list


def get_main_player(lineup_html):
    lineup = lineup_html.find('div', class_='large-7 aufstellung-vereinsseite columns small-12 unterueberschrift aufstellung-unterueberschrift').text.strip().split(':')[-1].strip()
    team_map = lineup_html.find('div', class_='large-7 columns small-12 aufstellung-vereinsseite')
    player_list_html = team_map.find_all('div', class_='aufstellung-spieler-container')
    player_list = []

    for i, player in enumerate(player_list_html):
        number = player.find('div' , class_='tm-shirt-number tm-shirt-number--large tm-shirt-number--bordered').text.strip()
        a_tag = player.find('a')
        name = a_tag.text.strip()
        url = a_tag.get('href')
        style = player.get('style')
        top = int(style.split(';')[0].split(':')[-1].strip()[:-1])
        player_data = {
            'name': name,
            'number': number,
            'url': url
        }
        if top < 10:
            player_data['state'] = 'attacker'

        elif top < 50:
            player_data['state'] = 'center'

        elif top < 79:
            player_data['state'] = 'defense'

        else:
            player_data['state'] = 'gatekeeper'

        player_list.append(player_data)


    return {
        "lineup": lineup,
        "main_player": player_list
    }


def get_substitutes(html_data):
    substitutes = html_data.find('table')
    rows = substitutes.find_all('tr')
    substitutes_list =[]
    for row in rows:
        tds = row.find_all('td')
        data = {
            "number" : tds[0].find('div').text,
            "name" : tds[1].find('a').get('title').strip(),
            "url" : tds[1].find('a').get('href'),
            "state" : tds[2].text.strip(),
        }
        substitutes_list.append(data)
    return substitutes_list


def get_lineups(soup):
    home_lineup = soup.find('div', class_='large-6 columns aufstellung-box')
    guest_lineups = soup.find('div', class_='large-6 columns')

    return {
        "home_data": get_main_player(home_lineup),
        "guest_data": get_main_player(guest_lineups),
        "home_substitutes": get_substitutes(home_lineup),
        "guest_substitutes": get_substitutes(guest_lineups)
    }


