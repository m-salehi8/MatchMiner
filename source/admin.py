from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Source, LeagueLinks, LeagueSeasonLinks, MatchLinks

@admin.register(Source)
class SourceAdmin(ModelAdmin):
    list_display = ('name', 'base_url', 'status', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('status',)

class LeagueSeasonLinksInline(TabularInline):
    model = LeagueSeasonLinks
    extra = 0

@admin.register(LeagueLinks)
class LeagueLinksAdmin(ModelAdmin):
    list_display = ('name', 'start_year', 'end_year')
    search_fields = ('name',)
    inlines = [LeagueSeasonLinksInline]

class MatchLinksInline(TabularInline):
    model = MatchLinks
    extra = 0

@admin.register(LeagueSeasonLinks)
class LeagueSeasonLinksAdmin(ModelAdmin):
    list_display = ('league', 'year', 'match_count', 'url')
    search_fields = ('league__name',)
    inlines = [MatchLinksInline]
    filter_display = ["league", "year"]

@admin.register(MatchLinks)
class MatchLinksAdmin(ModelAdmin):
    list_display = ('title', 'match_id', 'status', 'is_done', 'session')
    search_fields = ('title', 'match_id')
    list_filter = ('status', 'is_done', 'session__league', 'session__year')
