from django.contrib import admin

from .models import TradePoint, Operator, Game, Error, BulletHistory
admin.site.register(BulletHistory)
admin.site.register(Operator)
from pprint import pprint as p

class DurationFilter(admin.ListFilter):
	title = 'Продолжительность'
	parameter_name = 'duration'
	template = 'stats/custom_filter.html'

	def lookups(self, request, model_admin):
		#return (('80s', ('in the eighties')), ('90s', ('in the nineties')), )
		return (
			('foo','bar',),
		)

	def queryset(self, request, queryset):
		return queryset

	def has_output(self):
		return True


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
	list_display = ('label', 'name', 'address', 'status', 'game_count', 'interruptions', 'bulletsCount', 'big_toys_count', 'small_toys_count')
	inlines = [OperatorInline, GameInline]


class GameAdmin(admin.ModelAdmin):
	class Meta:
		verbose_name = 'Игры'


	list_display = ('get_label', 'start_time', 'duration', 'target', 'idle_count', 'prise', 'interrupt', 'service')
	list_filter = (
		#'interrupt', 'idle_count', 'start_time', 'trade_point__name',
		 DurationFilter,
		)
	#search_fields = ('duration', )

	def get_label(self, instance):
		return instance.trade_point.label
	get_label.short_description = 'ТТ'


class ErrorAdmin(admin.ModelAdmin):
	readonly_fields = ('params', 'output')
	class Meta:
		verbose_name = 'Ошибки'




admin.site.register(TradePoint, TradePointAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Error, ErrorAdmin)