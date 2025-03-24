from source.models import LeagueLinks, MatchLinks, Source, LeagueSeasonLinks
from crawler.scripts.index import crawl_data_sheet
from crawler.models import *
from crawler.scripts.club import get_data_club
from crawler.scripts.stik import get_stik
from crawler.scripts.time import get_time
from crawler.scripts.lineups import get_data_line
import time
import threading
from django.db import connection
source = Source.objects.all().first()


def get_matches(league_name, year=None):

    d = 0
    league = LeagueLinks.objects.filter(source=source, name=league_name).first()
    sessions = LeagueSeasonLinks.objects.filter(league=league).order_by("-year")
    if year:
        sessions = sessions.filter(year=year)
        print("***************************************           ", sessions.count())
    for session in sessions:
        matches = MatchLinks.objects.filter(session=session, is_done=False)
        for match in matches:
            print(match)
            mc = MatchCrawl.objects.filter(match=match, source=source).first()
            if not mc:
                mc = MatchCrawl()
                mc.match = match
                mc.source = source
                mc.save()
                print("saveeeeeeeeeee")

def get_url(tab, url):
    tab_list = {
        "club": "vorbericht",
        "stik": "statistik",
        "line": "aufstellung",
    }
    tab = tab_list.get(tab)
    if tab:
        url = url.replace("index", tab)

    return url


def crawl_index(match):
    data = crawl_data_sheet(match.match.url)
    if data:
        index_obj = IndexTab.objects.filter(match=match).first()
        if not index_obj:
            index_obj = IndexTab()

        index_obj.match = match
        index_obj.crawl_data = data
        index_obj.save()
        match.has_index = True
        match.save()


def crawl_lineups(match):
    url = get_url("line", match.match.url)
    data = get_data_line(url)
    if data:
        ins = LineUpsTab.objects.filter(match=match).first()
        if not ins:
            ins = LineUpsTab()

        ins.match = match
        ins.crawl_data = data
        ins.save()
        match.has_line = True
        match.save()




def crawl_statics(match):
    url = get_url("stik", match.match.url)
    data = get_stik(url)

    if data:
        ins = StatisticsTab.objects.filter(match=match).first()
        if not ins:
            ins = StatisticsTab()

        ins.match = match
        ins.crawl_data = data
        ins.save()
        match.has_stik = True
        match.save()


def crawl_club(match):
    url = get_url("club", match.match.url)
    data = get_data_club(url)
    if data:
        ins = ClubTab.objects.filter(match=match).first()
        if not ins:
            ins = ClubTab()

        ins.match = match
        ins.crawl_data = data
        ins.save()
        match.has_club = True
        match.save()


def crawl_time(match):
    data = get_time(match.match.url)
    if data:
        ins = TimeLineTab.objects.filter(match=match).first()
        if not ins:
            ins = TimeLineTab()

        ins.match = match
        ins.crawl_data = data
        ins.save()
        match.has_time = True
        match.save()


def crawl_match(match):
    if not match.has_stik:
        try:
            crawl_statics(match)
        except Exception as e:
            print("eeeeee  =======>>>     ", e)

    if not match.has_index:
        try:
            crawl_index(match)
        except Exception as e:
            print("eeeeee  =======>>>     ", e)


    if not match.has_club:
        try:
            crawl_club(match)
        except Exception as e:
            print("eeeeee  =======>>>     ", e)


    if not match.has_line:
        try:
            crawl_lineups(match)
        except Exception as e:
            print("eeeeee  =======>>>     ", e)

    if not match.has_time:
        try:
            crawl_time(match)
        except Exception as e:
            print("eeeeee  =======>>>     ", e)


def chunk_queryset(queryset, num_chunks=10):
    total_count = queryset.count()
    chunk_size = (total_count // num_chunks) + (1 if total_count % num_chunks else 0)
    return [queryset[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]


def process_chunk(chunk, chunk_index):
    print(f"Processing Chunk {chunk_index} - {chunk.count()} records")

    for obj in chunk:
        print(f"Processing {obj.id} in Chunk {chunk_index}")
        crawl_match(obj)

    connection.close()


def run():
#    matches = MatchCrawl.objects.filter(match__session__league__name='UEFA Conference League')  #all()[82800:83000]
#    matches =  MatchCrawl.objects.filter(match__session__league__name='LaLiga')[5_000:10_000]


    crawl_data = MatchCrawl.objects.filter(
        has_index=False, has_line=False, has_stik=False, has_club=False, has_time=False,
    )
    matches = crawl_data[10001:20000]
    
    
    chunked_matches = chunk_queryset(matches, num_chunks=12)

#    chunked_matches = chunk_queryset(matches)
#
    threads = []
    for i, chunk in enumerate(chunked_matches):
        thread = threading.Thread(target=process_chunk, args=(chunk, i))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("✅ All chunks processed.")

#start_time = time.time()

run()

#end = time.time() - start_time
#print("---  seconds ---     ", end)
#get_matches("Netherland Eredivisie")
#get_matches("UEFA Europa League")
#get_matches("UEFA Champions League")
#get_matches("Bundesliga")

