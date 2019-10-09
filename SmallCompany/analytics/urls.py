from django.contrib import admin
from django.conf.urls import url, include
from .views import HomeView, DetailedView


app_name = 'analytics'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='AnalyticsView'),
    url(r'^user/', DetailedView.as_view(), name='DetailedView'),
    ]