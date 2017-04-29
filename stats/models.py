from django.db import models
import datetime

class TradePoint(models.Model):
	class Meta:
		verbose_name = 'Торговая точка'
		verbose_name_plural = 'Тороговые точки'
	name = models.CharField("Имя",max_length=200)
	region = models.CharField("Регион",max_length=200)
	city = models.CharField("Город",max_length=200)
	address = models.CharField("Адрес",max_length=600)
	open_time = models.TimeField("Время открытия",default=datetime.time(9,0,0))
	close_time = models.TimeField("Время закрытия",default=datetime.time(22,0,0))
	target_count = models.IntegerField('Количество мишеней', default=1)
	label = models.IntegerField('ID', default=1)

	def __str__(self):
		return self.name


class Operator(models.Model):
	class Meta:
		verbose_name = 'Оператор'
		verbose_name_plural = 'Операторы'
	name = models.CharField(max_length=200)
	trade_point = models.ForeignKey(TradePoint, on_delete=models.CASCADE)
	start_time = models.TimeField("Начало работы",default=datetime.time(9,0,0))
	end_time = models.TimeField("Конец работы",default=datetime.time(22,0,0))
	phone = models.CharField("Телефон", max_length=200)


class GameType(models.Model):
	pass


class Target(models.Model):
	class Meta:
		verbose_name = "Мишень"
		verbose_name_plural = "Мишени"
	trade_point = models.ForeignKey(TradePoint, on_delete=models.CASCADE)


#Точка тира`, `Мишень`, `Дата`, `Время`, `Время игры`, `Статистика упавших`, `Количество холостых`, `Приз`, `Прерывание`, `Служебные`) VALUES ('63001001', '5', '2017-02-01', '14:03:12', '99', '11010111010100100010', '1', '0', '0', '0');
class Game(models.Model):
	class Meta:
		verbose_name = "Игра"
		verbose_name_plural = "Игры"
	trade_point = models.ForeignKey(TradePoint, on_delete=models.CASCADE)
	target = models.IntegerField("Мишень")
	start_time = models.DateTimeField('Время начала')
	duration = models.DurationField('Продолжительность игры', default=datetime.timedelta(0))
	fallen_count = models.IntegerField("Упавшие")
	idle_count = models.IntegerField("Холостые")
	prise = models.BooleanField("Приз")
	interrupt = models.BooleanField("Прерывание")
	service = models.IntegerField("Служебные")


	def __str__(self):
		return 'Игра'


