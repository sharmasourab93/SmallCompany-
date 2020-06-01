from django.contrib import admin
from django.conf.urls import url, include
from .views import DriverSpendView, FuelSpendView,\
    TotalSpendView, AcrossSpendView, LandingView


app_name = "analytics"


urlpatterns = [
    url(r'^$', LandingView.as_view(), name='AnalyticsView'),
    url(r'^driver/$', DriverSpendView.as_view(), name='DriverSpendView'),
    url(r'^fuel/$', FuelSpendView.as_view(), name="FuelSpendView"),
    url(r'^month/$', TotalSpendView.as_view(), name="TotalSpendView"),
    url(r'^across/$', AcrossSpendView.as_view(), name="AcrossSpendView"),
    ]
