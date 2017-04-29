from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta

from .models import Game, TradePoint

#INSERT INTO `Tir`(`Точка тира`, `Мишень`, `Дата`, `Время`, `Время игры`, `Статистика упавших`,
 #`Количество холостых`, `Приз`, `Прерывание`, `Служебные`) VALUES ([value-1],[value-2],[value-3],[value-4],[value-5],[value-6],[value-7],[value-8],[value-9],[value-10])

#TT=63001000&Mishen=1&Date="2017-4-29"&Time="	15:16:33"&GameTime=18&
#Stat="00000000000000000000"&Hol=3&Priz=0&Stop=0&Other=0

def cleanInput(string):
	return string.replace('"', '');
def getDataFromUrl(req):
	get = lambda name, default: cleanInput(req.get(name, default))
	result = {}
	skipFields = ('Date', 'Time', 'TT')
	mapUrlToProps = {
		'Mishen': 'target',
		'GameTime': 'duration',
		'Stat': 'fallen_count',
		'Hol': 'idle_count',
		'Priz': 'prise',
		'Stop': 'interrupt',
		'Other': 'service',
	}
	for key, val in mapUrlToProps.items():
		if key in skipFields:
			continue
		result[val] = get(key, '')

	#return result
	result['trade_point'] = TradePoint.objects.get(label=get('TT', ''))

	dateFormat = '%Y-%m-%dT%H:%M:%S'
	result['start_time'] = datetime.strptime(
		get('Date','') + 'T' + get('Time', ''),
		dateFormat
	)

	result['duration']  = timedelta(0, int(result['duration']))
	return result


def insert(request):
	params = getDataFromUrl(request.GET)
	g = Game(**params)
	g.save()
	return HttpResponse("success")