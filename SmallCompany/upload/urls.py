from django.urls import path
from .views import LandingView, UploadView
from .views import PriceUpdation, DriverEnrollment, PurchaseUpdate
from .views import sign_up, login_user, logout, password_change

# login_required: This decorator module can be encircled to
# the method name in urls to impose login restrictions
# from django.contrib.auth.decorators import login_required
# For example :
# 5. Landing View can be encircles with login requirement
# path('', login_required(LandingView.as_view()), name="LandingView"),


app_name = 'upload'

urlpatterns = [
    
    # URL Routes to Handle Accounts Login/SignUp
    # 1. SignUp
    path('accounts/signup', sign_up, name="sign-up"),
    # 2. Login
    path('accounts/login', login_user, name="login"),
    # 3. Logout
    path('accounts/logout', logout, name="logout"),
    # 4. Password Change
    path('accounts/password-change', password_change, name="password_change"),
    
    # URL Routes' Logical View Functions
    # 5. Landing Point View
    path('', LandingView.as_view(), name="LandingView"),
    
    # 6. Purchase Update Record
    path('purchase/', PurchaseUpdate.as_view(), name="PurchaseUpdate"),
    
    # 7. Bulk Update View
    path('bulk/', UploadView.as_view(), name='UploadView'),
    
    # 8. Price Update View
    path('price/', PriceUpdation.as_view(), name="FuelPriceUpdate"),
    
    # 9. Driver Record Update
    path('driverRec/', DriverEnrollment.as_view(), name="DriverEnroll"),
    ]
