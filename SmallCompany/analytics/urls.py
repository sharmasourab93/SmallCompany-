from django.urls import path, re_path

# Section 2 View By Driver's Spend
from .views import DriverSpendView, FuelSpendView
from .views import DriverSpendDetails, DriverSpendByMonth

# Section 3 View By Fuel Spends
from .views import FuelSpendDetails, FuelSpendByMonth

# Section 4 Total Spend View  Specific Spend View Related Imports
from .views import TotalSpendView

# Section 5 Total Spend Specific Imports
from .views import TotalSpendSpecific, TotalSpendTimeSpecific

# 6. Visilizing View & Langing View Improt
from .views import AcrossSpendView, LandingView


app_name = "analytics"


urlpatterns = [
    # URL Routes for Analytics/Trend Reports
    # 1. Landing View On Analytics/Trends App
    path('', LandingView.as_view(), name='AnalyticsView'),
    
    # 2. Driver View
    path('driver/', DriverSpendView.as_view(), name='DriverSpendView'),
    # 2.a. Driver Spend Details
    re_path(r'^driver/(?P<driver_id_id>\d+)/$',
            DriverSpendDetails.as_view(), name="DriverSpendDetails"),
    # 2.b. Total Driver Spend By Month
    re_path(r'^driver/total/month/(?P<driver_id_id>\d+)/$',
            DriverSpendByMonth.as_view(), name="DriverSpendByMonth"),
    
    # 3. Fuel Spend View
    path('fuel/', FuelSpendView.as_view(), name="FuelSpendView"),
    # 3.a. Fuel Spend Details by Drivers across Fuel Types
    re_path(r'^fuel/(?P<fuel_id>\d)/$',
            FuelSpendDetails.as_view(), name="FuelSpendDetails"),
    # 3.b. Fuel Spend By Fuel Type
    re_path(r'^fuel/total/month/(?P<fuel_id>\d)/$',
            FuelSpendByMonth.as_view(), name="FuelSpendDetails"),
    
    # 4. Total Spend In A Month Across Categories
    path('spends/', TotalSpendView.as_view(), name="TotalSpendView"),
    
    # 5. Total Spends Across Fuels & Drivers Specific to Year & Month
    path('choose',
         TotalSpendSpecific.as_view(),
         name="TotalSpendSpecific"),
    re_path(r'year/(?P<year>\d{4})$',
            TotalSpendTimeSpecific.as_view(),
            name="TotalSpendTimeSpecific"),
    re_path(r'year/(?P<year>[0-9]{4})/'
            r'month/(?P<month>\d{1,2})$',
            TotalSpendTimeSpecific.as_view(),
            name="TotalSpendTimeSpecific_"),
    
    # 5. Overall Spend Analysis
    path('across/',
         AcrossSpendView.as_view(),
         name="VisualizeSpendView"),
    ]
