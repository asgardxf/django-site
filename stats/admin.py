from django.contrib import admin
from .models import TradePoint, Operator, Game
#admin.site.register(TradePoint)
admin.site.register(Operator)
from pprint import pprint as p


class OperatorInline(admin.TabularInline):
    model = Operator
    extra = 0

class GameInline(admin.TabularInline):
	model = Game
	extra = 0
	readonly_fields = ('start_time','duration', 'shotCount', 'target')
	fields = ('start_time','duration', 'shotCount', 'target')

	verbose_name = 'Игра'
	verbose_name_plural = 'Игры'
	def shotCount(self, instance):
		if instance.idle_count is None:
			return 0
		return 21 + instance.idle_count

	shotCount.short_description = 'Выстрелы'

	#fields = ('target',) shotCount


class TradePointAdmin(admin.ModelAdmin):
	list_display = ('label', 'name', 'address', 'status', 'game_count', 'interruptions', 'bulletsLeft')
	inlines = [OperatorInline, GameInline]


class GameAdmin(admin.ModelAdmin):
	class Meta:
		verbose_name = 'Статистика'


	list_display = ('get_label', 'start_time', 'duration', 'target', 'idle_count', 'prise', 'interrupt', 'service')

	def get_label(self, instance):
		return instance.trade_point.label
	get_label.short_description = 'ТТ'


admin.site.register(TradePoint, TradePointAdmin)
admin.site.register(Game, GameAdmin)