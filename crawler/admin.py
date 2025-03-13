from django.contrib import admin
from unfold.admin import ModelAdmin
from crawler.models import MatchCrawl, IndexTab, LineUpsTab, StatisticsTab, ClubTab, TimeLineTab

@admin.register(MatchCrawl)
class MatchCrawlAdmin(ModelAdmin):
    list_display = ( 'match', 'created_at', 'updated_at')
    raw_id_fields = ("match",)


@admin.register(IndexTab)
class IndexTabAdmin(ModelAdmin):
    list_display = ('match', 'is_valid', 'created_at', 'updated_at')
    search_fields = ('match__match__match_id',)
    list_filter = ('is_valid',)


@admin.register(LineUpsTab)
class LineUpsTabAdmin(ModelAdmin):
    list_display = ('match', 'is_valid', 'created_at', 'updated_at')
    search_fields = ('match__match__match_id',)
    list_filter = ('is_valid',)


@admin.register(StatisticsTab)
class StatisticsTabAdmin(ModelAdmin):
    list_display = ('match', 'is_valid', 'created_at', 'updated_at')
    search_fields = ('match__match__match_id',)
    list_filter = ('is_valid',)


@admin.register(ClubTab)
class ClubTabAdmin(ModelAdmin):
    list_display = ('match', 'is_valid', 'created_at', 'updated_at')
    search_fields = ('match__match__match_id',)
    list_filter = ('is_valid',)


@admin.register(TimeLineTab)
class TimeLineTabAdmin(ModelAdmin):
    list_display = ( 'match', 'is_valid', 'created_at', 'updated_at')
    search_fields = ('match__match__match_id',)
    list_filter = ('is_valid',)
