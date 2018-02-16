from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta

from ..models import Game, TradePoint, Error, BulletHistory

def showTradePointStats(request, id):
    return render(request, 'stats/tradepoint_select_params.html', {'id': id})


def getFilterDate(period):
    relation = {
        'month': 30, 'week': 7, 'day': 1
    }
    daysCount = relation[period]
    return datetime.today() - timedelta(days=daysCount)


def getModel(_type):
    relation = {
        'game': Game, 'bullet': BulletHistory, 'prise': Game
    }
    return relation[_type]


def plotGame(data):
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as pl
    from collections import Counter
    import io
    c = Counter(x[0] for x in data)
    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.bar(c.keys(), c.values(), width=.1)
    # ax.bar(['foo','bar'], [1,5], width=.1)
    # ax.xaxis_date()
    buf = io.BytesIO()
    fig.autofmt_xdate()
    fig.savefig(buf, format='png')
    buf.seek(0)
    v = buf.getvalue()
    buf.close()
    return v


def plotBullets(data):
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as pl
    from collections import Counter
    import io
    d = dict()
    for (date, instance) in data:
        if date not in d:
            d[date] = 0
        d[date] += -(instance.bullet_count)

    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.bar(d.keys(), d.values(), width=.1)

    buf = io.BytesIO()
    fig.autofmt_xdate()
    fig.savefig(buf, format='png')
    buf.seek(0)
    v = buf.getvalue()
    buf.close()
    print(data)
    return v


plots = {'game': plotGame, 'bullet': plotBullets, 'prise': plotGame}


def tradePointStats(request, id):
    period = getFilterDate(request.GET.get('period'))
    params = {'trade_point': id, 'start_time__gte': period}
    _type = request.GET.get('type')
    if _type == 'prise':
        params['prise'] = True
    objects = getModel(_type).objects.filter(**params)
    result = tuple((g.start_time.strftime("%d %h %H:%M"), g) for g in objects)
    file = plots[_type](result)
    return HttpResponse(file, content_type='image/png')
