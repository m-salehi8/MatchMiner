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
from myprofiler import profile



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
            # mc = MatchCrawl.objects.filter(match=match, source=source).first()
            # if not mc:
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
    print("__________________             INDEX   ______________________")



def crawl_lineups(match):
    url = get_url("line", match.match.url)
    data = get_data_line(url)
    print("__________________             LINE   ______________________")





def crawl_statics(match):
    url = get_url("stik", match.match.url)
    data = get_stik(url)
    print("__________________             STIK   ______________________")





def crawl_club(match):
    url = get_url("club", match.match.url)
    data = get_data_club(url)
    print("__________________             CLUB   ______________________")


def crawl_time(match):
    data = get_time(match.match.url)
    print("__________________             TIME   ______________________")




def crawl_match(match):
    try:
        crawl_statics(match)
    except Exception as e:
        print("eeeeee  =======>>>     ", e)

    try:
        crawl_index(match)
    except Exception as e:
        print("eeeeee  =======>>>     ", e)


    try:
        crawl_club(match)
    except Exception as e:
        print("eeeeee  =======>>>     ", e)


    try:
        crawl_lineups(match)
    except Exception as e:
        print("eeeeee  =======>>>     ", e)

    try:
        crawl_time(match)
    except Exception as e:
        print("eeeeee  =======>>>     ", e)


# 82 800:83 000

def chunk_queryset(queryset, num_chunks=48):
    total_count = queryset.count()
    chunk_size = (total_count // num_chunks) + (1 if total_count % num_chunks else 0)
    return [queryset[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]


def process_chunk(chunk, chunk_index):
    print(f"Processing Chunk {chunk_index} - {chunk.count()} records")

    for obj in chunk:
        print(f"Processing {obj.id} in Chunk {chunk_index}")
        crawl_match(obj)

    connection.close()

@profile
def run():
    crawl_data = MatchCrawl.objects.filter(
       has_index=True, has_line=True, has_stik=True, has_club=True, has_time=True,
    )
    matches = crawl_data[401:600]
    chunked_matches = chunk_queryset(matches, num_chunks=48)

    threads = []
    for i, chunk in enumerate(chunked_matches):
        thread = threading.Thread(target=process_chunk, args=(chunk, i))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("✅ All chunks processed.")

#start_time = time.time()
#if __name__ == "__main__":

run()
#end = time.time() - start_time
#print("---  seconds ---     ", end)
#get_matches("Serie A")
#get_matches("Bundesliga")

