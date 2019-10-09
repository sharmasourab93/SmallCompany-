from django.contrib import admin
from .models import DriverDetails, PurchaseRecord
from .models import FuelType, FuelPrice


admin.site.register(DriverDetails)
admin.site.register(PurchaseRecord)
admin.site.register(FuelPrice)
admin.site.register(FuelType)

