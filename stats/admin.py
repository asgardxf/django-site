from django.contrib import admin

from .models import TradePoint, Operator, Game, Error, BulletHistory
admin.site.register(BulletHistory)
from pprint import pprint as p
import datetime

class DurationFilter(admin.SimpleListFilter):
	title = 'Продолжительность'
	parameter_name = 'duration'

	params_map = {
			'1m':1,
			'3m':3,
			'5m':5,
			'7m':7,
			'10m':10,
			'15m':15,
	}

	def lookups(self, request, model_admin):
		return (
			('1m','1 минута',),
			('3m','3 минуты',),
			('5m','5 минут',),
			('7m','7 минут',),
			('10m','10 минут',),
			('15m','15 минут',),
		)

	def queryset(self, request, queryset):
		minutes_count = self.params_map.get(self.value())
		if minutes_count:
			return queryset.filter(duration__gt= datetime.timedelta(minutes=minutes_count))
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


class OperatorAdmin(admin.ModelAdmin):
	list_display = ('name', 'trade_point', 'start_time', 'end_time', 'phone')

class TradePointAdmin(admin.ModelAdmin):
	list_display = ('label', 'name', 'address', 'status', 'game_count', 'interruptions', 'bulletsCount', 'big_toys_count', 'small_toys_count')
	inlines = [OperatorInline, GameInline]

def idle_render(obj):
	i = obj.idle_count
	colors = {
		0: 'blue', 1: 'green', 2: 'yellow',
	}
	color = colors.get(i, 'red')
	return '<span style="color: {};">{}</span>'.format(color, i)

idle_render.short_description = 'Холостые'
idle_render.allow_tags = True

class GameAdmin(admin.ModelAdmin):
	class Meta:
		verbose_name = 'Игры'


	list_display = ('get_label', 'start_time', 'duration', 'target', idle_render, 'prise', 'interrupt', 'service')
	list_filter = (
		'interrupt', 'idle_count', 'start_time', 'trade_point__name',
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
admin.site.register(Operator, OperatorAdmin)