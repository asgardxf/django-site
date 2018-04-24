from django.contrib import admin
from django.utils.html import format_html
from django.db.models.expressions import RawSQL
import datetime

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
    'label', 'name', 'region', 'city', 'address', 'status', 'game_count', 'interruptions', 'bulletsCount', 'big_toys_count',
    'small_toys_count', 'stats')
    inlines = [GameInline]

    def stats(self, instance):
        return format_html('<a href="/showStats/trade_point/{}" target="_blank">Статистика</a>', instance.id)

    stats.short_description = 'Статистика'


class MonitoringModel(TradePoint):
    class Meta:
        proxy = True
        verbose_name = 'Мониторинг'
        verbose_name_plural = 'Мониторинг'


@admin.register(MonitoringModel)
class Monitoring(admin.ModelAdmin):
    list_display = ('name', 'game_count', 'correct_game_count', 'bullets', 'prise')
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    def get_queryset(self, request):
        today = str(datetime.date.today())
        qs = TradePoint.objects.annotate(
            game_count=RawSQL(
                'select count(*) from stats_game g '
                'where g.trade_point_id = stats_tradepoint.id and g.start_time > date(%s)', [today]
            ),
            correct_game_count=RawSQL(
                'select count(*) from stats_game g '
                'where g.trade_point_id = stats_tradepoint.id and g.start_time > date(%s) and not interrupt', [today]
            ),
            bullets=RawSQL(
                'select sum(bullet_count) from stats_bullethistory b '
                'where b.trade_point_id = stats_tradepoint.id and b.start_time > date(%s)',
                [today]
            ),
            prise=RawSQL(
                'select sum(1) from stats_game g '
                'where g.trade_point_id = stats_tradepoint.id and g.start_time > date(%s) and prise', [today]
            ),
        )
        return qs

    def game_count(self, obj):
        return obj.game_count
    game_count.short_description = 'Всего игр'

    def correct_game_count(self, obj):
        return obj.correct_game_count
    correct_game_count.short_description = 'Завершённых игр'

    def bullets(self, obj):
        return obj.bullets
    bullets.short_description = 'Пули'

    def prise(self, obj):
        return obj.prise
    prise.short_description = 'Призы'