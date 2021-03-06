from django.contrib import admin

from ..models import TradePoint, Operator, Game, Error, BulletHistory


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'phone')


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    readonly_fields = ('params', 'output')

    class Meta:
        verbose_name = 'Ошибки'


@admin.register(BulletHistory)
class BulletAdmin(admin.ModelAdmin):
    list_display = ['trade_point', 'bullet_count', 'start_time']