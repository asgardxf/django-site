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
	def shotCount(self, instance):
		if instance.idle_count is None:
			return 0
		return 21 + instance.idle_count

	shotCount.short_description = 'Выстрелы'

	#fields = ('target',) shotCount


class TradePointAdmin(admin.ModelAdmin):
	list_display = ('label', 'name', 'address', 'status', 'game_count', 'interruptions')
	inlines = [OperatorInline, GameInline]


admin.site.register(TradePoint, TradePointAdmin)