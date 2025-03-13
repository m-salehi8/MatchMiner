# from django.contrib import admin
# from unfold.admin import ModelAdmin, TabularInline
# from .models import LeagueData, TeamData, StadiumData, RefereeData, MatchData
#
# class LeagueMatchDataInline(TabularInline):
#     model = MatchData
#     extra = 0
#
# @admin.register(LeagueData)
# class LeagueDataAdmin(ModelAdmin):
#     list_display = ('name', 'country', 'year', 'source')
#     search_fields = ('name', 'country')
#     inlines = [LeagueMatchDataInline]
#
# class HomeMatchesInline(TabularInline):
#     model = MatchData
#     fk_name = 'home_team'
#     extra = 0
#
# class AwayMatchesInline(TabularInline):
#     model = MatchData
#     fk_name = 'away_team'
#     extra = 0
#
# @admin.register(TeamData)
# class TeamDataAdmin(ModelAdmin):
#     list_display = ('name', 'url', 'composition', 'source')
#     search_fields = ('name',)
#     inlines = [HomeMatchesInline, AwayMatchesInline]
#
# class StadiumMatchDataInline(TabularInline):
#     model = MatchData
#     fk_name = 'stadium'
#     extra = 0
#
# @admin.register(StadiumData)
# class StadiumDataAdmin(ModelAdmin):
#     list_display = ('name', 'url', 'attendance')
#     search_fields = ('name',)
#     inlines = [StadiumMatchDataInline]
#
# class RefereeMatchDataInline(TabularInline):
#     model = MatchData
#     fk_name = 'referee'
#     extra = 0
#
# @admin.register(RefereeData)
# class RefereeDataAdmin(ModelAdmin):
#     list_display = ('name', 'url')
#     search_fields = ('name',)
#     inlines = [RefereeMatchDataInline]
#
# @admin.register(MatchData)
# class MatchDataAdmin(ModelAdmin):
#     list_display = ('league', 'home_team', 'away_team', 'match_date', 'home_score', 'away_score')
#     search_fields = ('home_team__name', 'away_team__name')
#     list_filter = ('league',)
