from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import DetailView
from upload.models import FuelPrice, FuelType
from upload.models import DriverDetails, PurchaseRecord
from .forms import HomeForm


class HomeView(TemplateView):
    
    template_name = 'analytics/home.html'
    model = PurchaseRecord
    
    dd_model = DriverDetails
    
    def get(self, request, **kwargs):
        
        form = HomeForm()
        
        return render(request,
                      self.template_name,
                      {'form': form})
    
    def post(self, request, **kwargs):
        
        form = HomeForm(request.POST)
        
        if form.is_valid():
            
            driver = form.cleaned_data['driver']
            dd_query = self.dd_model.objects.filter(serial_id=driver)[0]
            
            pr_query = self.model.objects.filter(driver_id=dd_query)
            
            models = pr_query
            return render(request,
                          self.template_name,
                          {'form': form,
                           'model': models}
                          )
        
        else:
            text = "No records found."
            
            return render(request,
                          self.template_name,
                          {'form': form,
                           'text': text})
        
    

class DetailedView(DetailView):
    
    template_name = 'analytics/details.html'
    model = DriverDetails