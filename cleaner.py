from crawler.models import *

def get_data():
    crawl_data = MatchCrawl.objects.filter(
        has_index=True, has_line=True, has_stik=True, has_club=True, has_time=True,
    )
    c = crawl_data.count()
    for match in crawl_data:
        try:
            print("===>>>>>>>>>      ", c)
            c -= 1
            index_data = IndexTab.objects.filter(match=match).first()
            stik_data = StatisticsTab.objects.filter(match=match).first()
            club_data = ClubTab.objects.filter(match=match).first()
            time_data = TimeLineTab.objects.filter(match=match).first()
            line_data = LineUpsTab.objects.filter(match=match).first()

            cleen = CleanData.objects.filter(match=match).first()
            if not cleen:
                cleen = CleanData()

            cleen.match = match
            cleen.match_pk = match.match.match_id
            cleen.title = match.match.title
            cleen.year = match.match.session.year
            cleen.league_name = match.match.session.league.name
            cleen.statistics = stik_data.crawl_data
            cleen.league = index_data.crawl_data['league']
            cleen.related_data = index_data.crawl_data['related_data']
            stadium = {
                "title": index_data.crawl_data['match_result']['stadium']['name'],
                "url": index_data.crawl_data['match_result']['stadium']['url'],
                "attendance": index_data.crawl_data['match_result']['attendance'],
            }
            cleen.stadium = stadium

            referee = {
                "title": index_data.crawl_data['match_result']['stadium']['referee'],
                "url": index_data.crawl_data['match_result']['stadium']['referee_url'],
                "assist":"",
            }
            cleen.referee = referee
            result = {
                "end": index_data.crawl_data['match_result']['end_result'],
                "over": index_data.crawl_data['match_result']['match_result'],
            }
            cleen.result = result
            home_team = line_data.crawl_data['teams'][0]
            home_team.update({
                "index": index_data.crawl_data['teams']['home_team']
            })
            cleen.home_team = home_team

            away_team = line_data.crawl_data['teams'][1]
            away_team.update({
                "index": index_data.crawl_data['teams']['guest_team']
            })
            cleen.away_team = away_team
            cleen.club = club_data.crawl_data
            cleen.cards = time_data.crawl_data['cards']
            cleen.goals = time_data.crawl_data['goals']
            cleen.substitutions = time_data.crawl_data['substitutions']
            cleen.match_date = index_data.crawl_data['match_result']['date']

            cleen.save()

        except Exception as e:
            print("=============>>>>>>>>        ", e)
            print(match)
            print("____________________________________________")







CleanData.objects.all().delete()
get_data()
