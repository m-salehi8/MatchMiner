from crawler.models import *
from source.models import *


league = LeagueSeasonLinks.objects.filter(league__name="Premier League", year__in=[2023, 2020, 2000])
pleague = LeagueSeasonLinks.objects.filter(league__name="LaLiga", year__in=[2024, 2017, 1990])

all = []
for l in league:
    all.append(l)
    
for n in pleague:
    all.append(n)
    
    
print(len(all))
