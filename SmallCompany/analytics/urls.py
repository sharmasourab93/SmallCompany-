from django.contrib import admin
from django.conf.urls import url, include
from .views import HomeView

urlpatterns = [
    url('^$', HomeView.as_view(), name='AnalyticsView')
    ]