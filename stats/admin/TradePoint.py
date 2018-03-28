from django.contrib import admin
from django.utils.html import format_html

from ..models import TradePoint, Operator, Game


class OperatorInline(admin.TabularInline):
    model = Operator
    extra = 0


class GameInline(admin.TabularInline):
    model = Game
    extra = 0
    readonly_fields = ('start_time', 'duration', 'shotCount', 'target')
    fields = ('start_time', 'duration', 'shotCount', 'target')

    verbose_name = 'Игра'
    verbose_name_plural = 'Игры'

    def shotCount(self, instance):
        if instance.idle_count is None:
            return 0
        return 21 + instance.idle_count

    shotCount.short_description = 'Выстрелы'


@admin.register(TradePoint)
class TradePointAdmin(admin.ModelAdmin):
    list_display = (
    'label', 'name', 'address', 'status', 'game_count', 'interruptions', 'bulletsCount', 'big_toys_count',
    'small_toys_count', 'stats')
    inlines = [GameInline]

    def stats(self, instance):
        return format_html('<a href="/showStats/trade_point/{}" target="_blank">Статистика</a>', instance.id)

    stats.short_description = 'Статистика'