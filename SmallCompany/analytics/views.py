# Django URL/Rendering View Functionality imports.
from django.shortcuts import render, redirect, Http404
from django.shortcuts import get_object_or_404, HttpResponse

# View/Template Import
from django.views.generic import TemplateView
from django.views.generic import DetailView

# Imports from Models.
from SmallCompany.upload.models import FuelPrice, FuelType
from SmallCompany.upload.models import DriverDetails, PurchaseRecord

# Imports Related to Forms.
from .forms import DriverSpendForm


class LandingView(TemplateView):
    template_name = 'analytics/analytics.html'
    
    
class DriverSpendView(TemplateView):
    
    template_name = 'analytics/driver.html'
    model = PurchaseRecord
    
    dd_model = DriverDetails
    
    def get(self, request, **kwargs):
        
        form = DriverSpendForm()
        
        return render(request,
                      self.template_name,
                      {'form': form})
    
    #TODO: Fix Post View of Spend By Driver
    def post(self, request, **kwargs):
        
        form = DriverSpendForm(request.POST)
        
        if form.is_valid():
            
            driver = form.cleaned_data['driver']
            try:
                dd_query = self.dd_model.objects.filter(serial_id=driver)
                pr_query = self.model.objects.filter(driver_id=dd_query)
            except ValueError:
                return Http404(request)
            
            models = pr_query
            return render(request,
                          self.template_name,
                          {'form': form,
                           'models': models}
                          )
        
        else:
            text = "No records found."
            
            return render(request,
                          self.template_name,
                          {'form': form,
                           'text': text})


class FuelSpendView(TemplateView):
    
    template_name = 'analytics/details.html'
    model = PurchaseRecord

    def get(self, request, **kwargs):
        form = DriverSpendForm()
        return render(request, self.template_name,
                      {'form': form})
    

class TotalSpendView(TemplateView):
    template_name = 'analytics/totalspend.html'


class AcrossSpendView(TemplateView):
    template_name = 'analytics/across.html'
