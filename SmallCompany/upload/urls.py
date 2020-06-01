from django.conf.urls import url
from .views import HomeView, UploadView, LandingView
from .views import PriceUpdation, DriverEnrollment


app_name = 'upload'

urlpatterns = [
    url(r'^$', LandingView.as_view(), name="LandingView"),
    url(r'^single/$', HomeView.as_view(), name='UpdateView'),
    url(r'^bulk/$', UploadView.as_view(), name='UploadView'),
    url(r'^price/$', PriceUpdation.as_view(), name="FuelPriceUpdate"),
    url(r'^driverRec/$', DriverEnrollment.as_view(), name="DriverEnroll")
    ]

