from django.db import models, connection
import datetime


class TradePoint(models.Model):
    class Meta:
        verbose_name = 'Торговую точку' #в родительном падеже
        verbose_name_plural = 'Торговые точки'

    name = models.CharField("Торговая точка", max_length=200)
    region = models.CharField("Регион", max_length=200)
    city = models.CharField("Город", max_length=200)
    address = models.CharField("Адрес", max_length=600)
    open_time = models.TimeField("Время открытия", default=datetime.time(9, 0, 0))
    close_time = models.TimeField("Время закрытия", default=datetime.time(22, 0, 0))
    target_count = models.IntegerField('Количество мишеней', default=1)
    label = models.IntegerField('ID', default=1, unique=True)
    capacity = models.IntegerField('Вместимость пуль', default=0)
    remaining_amount = models.FloatField('Оставшееся количество', default=0)
    big_toys_count = models.IntegerField('Большие игрушки', default=0)
    small_toys_count = models.IntegerField('Маленькие игрушки', default=0)

    def __str__(self):
        return self.name

    def filteredGameSetCount(self, **kvargs):
        return self.game_set.filter(**kvargs).count()

    def status(self):
        return self.filteredGameSetCount(start_time__range=[
            datetime.datetime.now() - datetime.timedelta(minutes=30), datetime.datetime.now()
        ]) > 0

    def game_count(self):
        return self.filteredGameSetCount(start_time__range=[
            datetime.date.today(), datetime.datetime.now()
        ])

    def interruptions(self):
        interruptCount = self.filteredGameSetCount(start_time__range=[
            datetime.date.today(), datetime.datetime.now()
        ], interrupt=False)
        if interruptCount == 0:
            return "Нет"
        return interruptCount

    def bulletsCount(self):
        with connection.cursor() as cursor:
            cursor.execute("select sum(bullet_count) from stats_bullethistory bh where bh.trade_point_id = %s",
                           [self.id])
            result = cursor.fetchone()
        return result[0]

    # def bulletsLeft(self):
    # 	return 'nan'
    # 	if self.capacity == 0:
    # 		return 'Не определено'
    # 	percentage = self.remaining_amount * 100 / self.capacity
    # 	if percentage > 100:
    # 		return '100%'
    # 	if percentage < 1:
    # 		return '0%'
    # 	return "{0:.1f}%".format(percentage)

    status.short_description = 'Работает'
    status.boolean = True

    game_count.short_description = 'Количество игр'

    interruptions.short_description = 'Прерывание'

    bulletsCount.short_description = 'Пули'


class BulletHistory(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['trade_point'], name='bullet_history_tp_idx')
        ]
        verbose_name = 'Приход пуль'
        verbose_name_plural = 'Приходы пуль'

    trade_point = models.ForeignKey(TradePoint, on_delete=models.CASCADE)
    bullet_count = models.IntegerField('Приход пуль', default=1)
    start_time = models.DateTimeField('Время прихода', default=datetime.datetime.now)


class Operator(models.Model):
    class Meta:
        verbose_name = 'Оператор'
        verbose_name_plural = 'Операторы'

    name = models.CharField(max_length=200)
    start_time = models.TimeField("Начало работы", default=datetime.time(9, 0, 0))
    end_time = models.TimeField("Конец работы", default=datetime.time(22, 0, 0))
    phone = models.CharField("Телефон", max_length=200)


class GameType(models.Model):
    pass


class Target(models.Model):
    class Meta:
        verbose_name = "Мишень"
        verbose_name_plural = "Мишени"

    trade_point = models.ForeignKey(TradePoint, on_delete=models.CASCADE)


# Точка тира`, `Мишень`, `Дата`, `Время`, `Время игры`, `Статистика упавших`, `Количество холостых`, `Приз`, `Прерывание`, `Служебные`) VALUES ('63001001', '5', '2017-02-01', '14:03:12', '99', '11010111010100100010', '1', '0', '0', '0');
class Game(models.Model):
    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Статистика"

    trade_point = models.ForeignKey(TradePoint, on_delete=models.CASCADE)
    target = models.IntegerField("Мишень")
    start_time = models.DateTimeField('Время начала')
    duration = models.DurationField('Продолжительность игры', default=datetime.timedelta(0))
    fallen_count = models.CharField("Упавшие", max_length=200)
    idle_count = models.IntegerField("Холостые")
    prise = models.BooleanField("Приз")
    interrupt = models.BooleanField("Прерывание")
    service = models.IntegerField("Служебные")

    def __str__(self):
        return 'Игра'


class Error(models.Model):
    class Meta:
        verbose_name = 'Ошибка'
        verbose_name_plural = 'Ошибки'

    params = models.TextField('Параметры')
    output = models.TextField('Сообщение')
