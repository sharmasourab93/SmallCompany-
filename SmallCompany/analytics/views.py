# Django URL/Rendering View Functionality imports.
from django.shortcuts import render, redirect, Http404
from django.shortcuts import get_object_or_404, HttpResponse, HttpResponseRedirect

# View/Template Import
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

# Imports from Models.
from upload.models import FuelPrice, FuelType
from upload.models import DriverDetails, PurchaseRecord

# Imports Related to Forms.
from .forms import DriverSpendForm, FuelSpendForm

# Importing Logger and other python core modules.
import logging


logger = logging.getLogger(__name__)


class LandingView(TemplateView):
    template_name = 'analytics/analytics.html'
    
    
class DriverSpendView(TemplateView):
    
    template_name = 'analytics/driver.html'
    model = PurchaseRecord
    dd_model = DriverDetails
    
    def get(self, request, **kwargs):
        logger.debug(str(__class__.__module__))
        form = DriverSpendForm()
        return render(request,
                      self.template_name,
                      {'form': form})
    
    def post(self, request, **kwargs):
        logger.debug(str(__class__.__module__))
        driver = request.POST.get('driver')
        dd_query = DriverDetails.objects.get(id=driver)
        logger.info("DD Query {}".format(str(dd_query)))
        logger.info("Before dd_query & pr_query {}"
                     .format(str(dd_query)))
        
        if dd_query is None:
            pr_query = PurchaseRecord.objects.filter(driver_id=dd_query)
            logger.info("Pr_query {}".format(dir(pr_query)))
            logger.info("No Value Error, HttpResponseRedirect")
        
        #TODO: Fix Redirection Issue in Drivers 1
        return redirect('/trends/driver/?driver=' + str(driver))
        

#TODO: Fix Redirection Issue in Drivers 1
class DriverSpendDetails(TemplateView):
    
    template_name = 'analytics/driver_details.html'
    model = PurchaseRecord
    
    def get(self, request, **kwargs):
        logger.info(str(__class__.__module__))
        obj = request.GET.get('driver')
        driver = DriverDetails.objects.get(id=obj)
        logger.info("In SPend details get method")
        if obj is not None:
            model = PurchaseRecord.objects.filter(driver_id=obj)
            return render(request,
                          self.template_name,
                          {'model': model})
        
        return render(request, self.template_name, {'model': None})
    

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
