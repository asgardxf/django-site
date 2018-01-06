from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta

from .models import Game, TradePoint, Error, BulletHistory

#INSERT INTO `Tir`(`Точка тира`, `Мишень`, `Дата`, `Время`, `Время игры`, `Статистика упавших`,
 #`Количество холостых`, `Приз`, `Прерывание`, `Служебные`) VALUES ([value-1],[value-2],[value-3],[value-4],[value-5],[value-6],[value-7],[value-8],[value-9],[value-10])

#TT=63001000&Mishen=1&Date="2017-4-29"&Time="	15:16:33"&GameTime=18&
#Stat="00000 00000 00000 00000"&Hol=3&Priz=0&Stop=0&Other=0

trade_point, idle_count, fallen_count, interrupt = ('trade_point','idle_count', 'fallen_count', 'interrupt')

def cleanInput(string):
	return string.replace('"', '');
def getDataFromUrl(req):
	get = lambda name, default: cleanInput(req.get(name, default))
	result = {}
	skipFields = ('Date', 'Time', 'TT')
	mapUrlToProps = {
		'Mishen': 'target',
		'GameTime': 'duration',
		'Stat': fallen_count,
		'Hol': idle_count,
		'Priz': 'prise',
		'Stop': 'interrupt',
		'Other': 'service',
	}
	for key, val in mapUrlToProps.items():
		if key in skipFields:
			continue
		result[val] = get(key, '')

	#return result
	result[trade_point] = TradePoint.objects.get(label=get('TT', ''))
	result[interrupt] = result[interrupt] == '0'

	dateFormat = '%Y-%m-%dT%H:%M:%S'
	result['start_time'] = datetime.strptime(
		get('Date','') + 'T' + get('Time', ''),
		dateFormat
	)

	result['duration']  = timedelta(0, int(result['duration']))
	return result


def insert(request):
	try:
		params = getDataFromUrl(request.GET)
		g = Game(**params)
		g.save()
		tp = params[trade_point]
		bh=BulletHistory(trade_point = tp, bullet_count  = -(20 + int(params[idle_count])))
		bh.save()
		results = params[fallen_count]
		if results.startswith('1'*20):
			tp.big_toys_count -= 1
		elif results.startswith('1'*15):
			tp.small_toys_count -= 1
		tp.save()
		return HttpResponse("success")
	except Exception as e:
		error = Error(params=request.META['QUERY_STRING'], output=repr(e))
		error.save()
		return HttpResponse("error")