
from crawler.models import CleanData
from match.models import *
from content.models import *

source =Source.objects.all().first()
def url_creator(path):
    return "https://www.transfermarkt.com" + path



def add_stadium(data):
    url = url_creator(data['url'])
    stadium_obj = Stadium.objects.filter(url=url).first()
    if not stadium_obj:
        stadium_obj = Stadium()
        stadium_obj.url = url
        stadium_obj.name = data['title'] if data['title'] != "" else "without name"
        stadium_obj.save()

    return stadium_obj



def add_referee(data):
    url = url_creator(data['url'])
    instance = Referee.objects.filter(url=url).first()
    if not instance:
        instance = Referee()
        instance.url = url
        instance.name = data['title'] if data['title'] != "" else "without name"
        instance.assistant = {}
        instance.save()

    return instance

def add_team(data):
    team = Team.objects.filter(name__iexact=data['name']).first()
    if not team:
        team = Team()
        team.name = data['name']
        team.url = ''
        team.logo = data['index']['icon']
        team.extra = data
        team.save()

    return team
def get_player(p):
    player = Player.objects.filter(name__iexact=p['name']).first()
    if not player:
        player = Player()
        player.name = p['name']
        player.url = url_creator(p['detail_url'])
        player.image = p['image_url']
        player.country = p['nationality']
        player.save()
    return player


def add_player(data, team):
    st = data['starting_lineup']['players']
    ss = data['substitutes']['players']
    for p in st:
        player = get_player(p)

        mp = MatchTeamPlayer.objects.filter(match_team=team, player=player).first()
        if not mp:
            mp = MatchTeamPlayer()
            mp.match_team = team
            mp.player = player
            mp.post = p['position']
            mp.main_player = True
            mp.number = p['number']
            mp.market_value = p['market_value']
            mp.is_captain = p['captain']
            mp.save()


    for p in ss:
        player = get_player(p)

        mp = MatchTeamPlayer.objects.filter(match_team=team, player=player).first()
        if not mp:
            mp = MatchTeamPlayer()
            mp.match_team = team
            mp.player = player
            mp.post ='' #data['position']
            mp.main_player = False
            mp.number = p['number']
            mp.market_value = p['market_value']
            mp.is_captain = p['captain']
            mp.save()



def add_manager(data):
    m = data['manager']
    manager = Manager.objects.filter(name__iexact=m['name']).first()
    if not manager:
        manager = Manager()
        manager.name = m['name']
        manager.url = url_creator(m['player_profile_url'])
        manager.image = m['image_url']
        manager.country = m['nationality']
        manager.save()
    return manager





def match_mapper():
    matches = CleanData.objects.all()
    for match in matches:
        stadium = add_stadium(match.stadium)
        ref = add_referee(match.referee)
        league = LeagueLinks.objects.filter(name=match.league_name).first()
        session =match.match.match.session
        ins = Match.objects.filter(match_id=match.match_pk, league=league, session=session).first()
        if not ins:
            ins = Match()
        ins.league = league
        ins.session = match.match.match.session
        ins.stadium = stadium
        ins.referee = ref
        ins.match_date = match.match_date[1]
        ins.match_day = match.match_date[0]
        ins.match_time = match.match_date[2]

        ins.home_score = match.result['over'].split(":")[0]
        ins.away_score = match.result['over'].split(":")[1]
        ins.match_id = match.match_pk
        ins.url = match.match.match.url
        s = {
            "crawl_id": match.id
        }
        ins.extra = s
        ins.statistics = match.statistics
        ins.club = match.club
        hg = []
        ag = []
        if match.goals:
            for g in match.goals:
                if g['team'] == 'home':
                    hg.append(g)

                if g['team'] == 'away':
                    ag.append(g)

        ins.home_goals = hg
        ins.away_goals = ag
        
        ch = []
        ca = []
        if match.cards:
            for m in match.cards:
                if m['team'] == 'home':
                    ch.append(m)
                
                if m['team'] == 'away':
                    ca.append(m)
                    
        ins.home_cards = ch
        ins.away_cards = ca
        

        home_team = add_team(match.home_team )
        away_team = add_team(match.away_team )

        home_manager = add_manager(match.home_team)
        away_manager = add_manager(match.away_team)

        
        ins.save()

        home_team = add_team(match.home_team )
        away_team = add_team(match.away_team )

        home_manager = add_manager(match.home_team)
        away_manager = add_manager(match.away_team)


        home_match = MatchTeam.objects.filter(match=ins, team=home_team).first()
        away_match = MatchTeam.objects.filter(match=ins, team=away_team).first()

        if not home_match:
            home_match = MatchTeam()
            home_match.match = ins
            home_match.team = home_team
            home_match.state = "home"
            if ins.home_score > ins.away_score:
                home_match.winner = True
            home_match.position = match.home_team['index']['position']
            home_match.goals = ins.home_score
            home_match.Manager = home_manager
            home_match.save()
            add_player(match.home_team , home_match)

            
            
        if not away_match:
            away_match = MatchTeam()
            away_match.match = ins
            away_match.team = away_team
            away_match.state = "away"
            if ins.away_score > ins.home_score:
                away_match.winner = True
            away_match.position = match.away_team['index']['position']
            away_match.goals = ins.away_score
            away_match.Manager = away_manager
            away_match.save()
            add_player(match.away_team , away_match)

match_mapper()

