from django.urls import path, re_path
from .views import DriverSpendView, FuelSpendView
from .views import DriverSpendDetails, DriverSpendByMonth
from .views import FuelSpendDetails, FuelSpendByMonth
from .views import TotalSpendView, AcrossSpendView, LandingView


app_name = "analytics"


urlpatterns = [
    # URL Routes for Analytics/Trend Reports
    # 1. Landing View On Analytics/Trends App
    path('', LandingView.as_view(), name='AnalyticsView'),
    
    # 2. Driver View
    path('driver/', DriverSpendView.as_view(), name='DriverSpendView'),
    # 2.a. Driver Spend Details
    re_path(r'^driver/(?P<driver_id_id>\d+)/$', DriverSpendDetails.as_view(), name="DriverSpendDetails"),
    # 2.b. Total Driver Spend By Month
    re_path(r'^driver/total/month/(?P<driver_id_id>\d+)/$', DriverSpendByMonth.as_view(), name="DriverSpendByMonth"),
    # 2.c. Fuel Spend By Year and Mont In One URL & One View
    # TODO: Fuel Spend By Year and Mont In One URL & One View
    # re_path()
    
    # 3. Fuel Spend View
    path('fuel/', FuelSpendView.as_view(), name="FuelSpendView"),
    # 3.a. Fuel Spend Details by Drivers across Fuel Types
    # path('fuel/<fuel_id>', FuelSpendDetail.as_view(), name="FuelSpendDetails"),
    # 3.b. Fuel Spend By Fuel Type
    # path('fuel/total/month/<fuel_id>', FuelSpendDetail.as_view(), name="FuelSpendDetails"),
    # 3.c Fuel Spend By Year and Month In One URL and One View
    # TODO: Fuel Spend By Year and Month In One URL and One View
    # path()
    
    # 4. Total Spend In  A Month Across Categories
    path('month/', TotalSpendView.as_view(), name="TotalSpendView"),
    
    # 5. Overall Spend Analysis
    path('across/', AcrossSpendView.as_view(), name="AcrossSpendView"),
    ]
