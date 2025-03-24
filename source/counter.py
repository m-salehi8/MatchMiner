
from source.models import *
from crawler.models import *

leagues = LeagueLinks.objects.all()
for league in leagues:
    matches = MatchLinks.objects.filter(session__league=league).count()
    print(matches)
    crawls = MatchCrawl.objects.filter(match__session__league=league)

    ss = crawls.filter(
        has_club=True, has_index=True, has_line=True, has_time=True, has_stik=True
    ).count()
    data = {
        "all": crawls.count(),
        "index": crawls.filter(has_index=True).count(),
        "lineups": crawls.filter(has_line=True).count(),
        "clubs": crawls.filter(has_club=True).count(),
        "stik": crawls.filter(has_stik=True).count(),
        "time": crawls.filter(has_time=True).count(),
    }
    league.match_count = matches
    league.complete_count = ss
    league.extra = data
    league.save()
