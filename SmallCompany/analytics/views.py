# Django URL/Rendering View Functionality imports.
from django.shortcuts import render, redirect, Http404, reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect

# View/Template Import
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import DetailView

# Imports from Models.
from upload.models import FuelPrice, FuelType
from upload.models import DriverDetails, PurchaseRecord

# Imports Related to Forms.
from .forms import DriverSpendForm, FuelSpendForm

# Importing Logger and other python core modules.
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


logger = logging.getLogger(__name__)


class LandingView(TemplateView):
    template_name = 'analytics/analytics.html'
    
    
class DriverSpendView(TemplateView):
    
    template_name = 'analytics/driver.html'
    model = PurchaseRecord
    dd_model = DriverDetails
    
    def get(self, request, **kwargs):
        logger.debug("In Get")
        form = DriverSpendForm()
        return render(request,
                      self.template_name,
                      {'form': form})
    
    def post(self, request, **kwargs):
        
        driver = request.POST.get('driver')
        
        return redirect('/trends/driver/' + str(driver))
        

class DriverSpendDetails(ListView):
    
    context = dict()
    template_name = 'analytics/driver_details.html'
    model = PurchaseRecord
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        id_ = self.kwargs['driver_id_id']
        
        context = super(DriverSpendDetails, self)\
            .get_context_data(**kwargs)
        
        purchase_record = PurchaseRecord.objects\
            .filter(driver_id_id=id_).order_by("dated")
        
        paginator = Paginator(purchase_record, self.paginate_by)
        page = self.request.GET.get('page')
        
        try:
            page_by = paginator.page(page)
        
        except PageNotAnInteger:
            page_by = paginator.page(1)
            
        except EmptyPage:
            page_by = paginator.page(paginator.num_pages)
            
        context['driver'] = DriverDetails.objects.get(id=id_).name
        context['purchase_record'] = page_by
        
        return context
    

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
