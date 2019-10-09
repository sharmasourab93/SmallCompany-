from django.conf.urls import url
from .views import HomeView, UploadView, LandingView


app_name = 'upload'

urlpatterns = [
    url(r'^$', LandingView.as_view(), name="LandingView"),
    url(r'^single/$', HomeView.as_view(), name='UpdateView'),
    url(r'^bulk/$', UploadView.as_view(), name='UploadView')
    ]

