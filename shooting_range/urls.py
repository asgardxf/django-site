"""shooting_range URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from stats.views.main import insert
from stats.views.stats import showTradePointStats, tradePointStats

statsPatterns = [
    path('trade_point/<int:id>', showTradePointStats),
    path('trade_point/result/<int:id>', tradePointStats)
]

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'insert.php/', insert),
    path(r'showStats/', include(statsPatterns)),
]
