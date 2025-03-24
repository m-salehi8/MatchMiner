from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import  Team, Stadium, Referee, Match, MatchTeam, MatchTeamPlayer, Player

class MatchTeamInline(TabularInline):
    model = MatchTeam
    extra = 0

class MatchStadiumInline(TabularInline):
    model = Stadium
    extra = 0

class MatchRefereeInline(TabularInline):
    model = Referee
    extra = 0

class MatchTeamPlayerInline(TabularInline):
    model = MatchTeamPlayer
    extra = 0



@admin.register(Team)
class TeamAdmin(ModelAdmin):
    # list_display = ('title', 'url', 'logo')
    # search_fields = ('title',)
    # inlines = [MatchTeamInline]
    pass


@admin.register(Stadium)
class StadiumAdmin(ModelAdmin):

    # list_display = ('name', 'url', 'capacity')
    # search_fields = ('name',)
    pass

@admin.register(Referee)
class RefereeAdmin(ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)


class MatchTeamIN(TabularInline):
    model = MatchTeam
    extra = 0
    tab= True


@admin.register(Match)
class MatchAdmin(ModelAdmin):
    list_display = ["league", "session", "stadium", "referee","match_id"]
    list_filter = ["league", "session", "referee", "stadium"]
    
    inlines = [MatchTeamIN]



#@admin.register(Match)
#class MatchAdmin(ModelAdmin):
#    pass
    # search_fields = ('title',)
    # inlines = [MatchTeamInline, MatchStadiumInline, MatchRefereeInline, MatchTeamPlayerInline]

@admin.register(MatchTeam)
class MatchTeamAdmin(ModelAdmin):
    # list_display = ('match', 'team', 'is_home_team', 'goals', 'winner', 'manager')
    # search_fields = ('team__title', 'match__title')
    # list_filter = ('is_home_team', 'winner')
    pass
@admin.register(MatchTeamPlayer)
class MatchTeamPlayerAdmin(ModelAdmin):
    # list_display = ('player', 'team', 'position', 'age', 'purchase_value', 'number')
    # search_fields = ('player__name', 'team__team__title')
    # list_filter = ('position',)
    pass



@admin.register(Player)
class PlayerAdmin(ModelAdmin):
    pass
    # search_fields = ('title',)
    # inlines = [MatchTeamInline, MatchStadiumInline, MatchRefereeInline, MatchTeamPlayerInline]
