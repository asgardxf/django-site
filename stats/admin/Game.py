from django.contrib import admin
from django.utils.html import format_html
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from ..models import Game

def idle_render(obj):
    i = obj.idle_count
    colors = {
        0: 'blue', 1: 'green', 2: 'yellow',
    }
    color = colors.get(i, 'red')
    return format_html('<span style="color: {};">{}</span>', color, i)


idle_render.short_description = 'Холостые'


class DurationFilter(admin.SimpleListFilter):
    title = 'Продолжительность'
    parameter_name = 'duration'

    params_map = {
        '1m': 1,
        '3m': 3,
        '5m': 5,
        '7m': 7,
        '10m': 10,
        '15m': 15,
    }

    def lookups(self, request, model_admin):
        return (
            ('1m', '1 минута',),
            ('3m', '3 минуты',),
            ('5m', '5 минут',),
            ('7m', '7 минут',),
            ('10m', '10 минут',),
            ('15m', '15 минут',),
        )

    def queryset(self, request, queryset):
        minutes_count = self.params_map.get(self.value())
        if minutes_count:
            return queryset.filter(duration__gt=datetime.timedelta(minutes=minutes_count))
        return queryset

    def has_output(self):
        return True


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'Игры'

    list_display = ('get_label', 'start_time', 'duration', 'target', idle_render, 'prise', 'interrupt', 'service')
    list_filter = (
        'interrupt', 'idle_count', ('start_time', DateRangeFilter), 'trade_point__name',
        DurationFilter,
    )

    # search_fields = ('duration', )

    def get_label(self, instance):
        return instance.trade_point.name


    get_label.short_description = 'ТТ'
