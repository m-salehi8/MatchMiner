import json
from source.models import *
with open("links.json", "r") as f:
    data = json.loads(f.read())


for r in data:
    try:
        league_name = r["league"]
        s = r["year"].split('-')[0]
        e = r["year"].split('-')[-1]
        q = "?saison_id={}&spieltagVon=1&spieltagBis=200"
        url = r['url'].replace("startseite", "gesamtspielplan")
        url += q
        source = Source.objects.all().first()
        m = LeagueLinks()
        m.source = source
        m.name = league_name
        m.start_year = s
        m.end_year = e
        m.url = url
        m.save()
        print(url)

    except Exception as e:
        print(e)
        continue
