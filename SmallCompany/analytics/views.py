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
from django.db.models import Count, Sum, F
from django.db.models.functions import ExtractMonth, ExtractYear

# Imports Related to Forms.
from .forms import DriverSpendForm, FuelSpendForm

# Importing Logger and other python core modules.
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


logger = logging.getLogger(__name__)


class LandingView(TemplateView):
    """Landing View For Analytics Section"""
    template_name = 'analytics/analytics.html'
    
    
class DriverSpendView(TemplateView):
    """
    Driver Spend View
        Handles two view functionalities based on HTTP Methods.
        1. GET - Gets the Page with DriverSpendForm
        2. POST - Submits the form with Option to Redirect to
            i. All Spend for a Driver
            ii. All Spends by the Driver on a month
    """
    template_name = 'analytics/ctemplate.html'
    model = PurchaseRecord
    dd_model = DriverDetails
    
    def get(self, request, **kwargs):
        logger.debug("In Get")
        form = DriverSpendForm()
        return render(request,
                      self.template_name,
                      {'form': form})
    
    def post(self, request, **kwargs):
        
        by_month = request.POST.get('by_month')
        driver = request.POST.get('driver')
        
        if by_month == '0':
            return redirect('/trends/driver/' + str(driver))
        
        elif by_month == '1':
            return redirect('/trends/driver/total/month/' + str(driver))
        

class DriverSpendDetails(ListView):
    """
    Driver Spend Details View (List View)
        This View is redirected from DriverSpendView's POST HTTP method
        This View retrieves all the records w.r.t.
        to the Driver's Unique ID.
    """
    
    context = dict()
    template_name = 'analytics/list_all_records_template.html'
    model = PurchaseRecord
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        id_ = self.kwargs['driver_id_id']
        
        context = super(DriverSpendDetails, self)\
            .get_context_data(**kwargs)
        
        # Django ORM based annotations to add a field
        # by the name Spent= Column(Field) * Column(Price)
        purchase_record = PurchaseRecord.objects\
            .filter(driver_id_id=id_)\
            .annotate(spent=F('price') * F('volume'))\
            .values('dated', 'volume',
                    'price', 'spent',
                    'fuel_type__name')\
            .order_by("dated")
        
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

#TODO: Add Spend URL & View By Year for driver
# Example 1: /trends/driver/year/2019/month/08/
# The above must extract records for 08-2019
# Example 2: /trends/driver/year/2019
# The above must extract all records by month for year 2019


class DriverSpendByMonth(ListView):
    """
    Driver Spend By Month (List View)
        This View shows the accumulated fuel spends by
        a driver identified by his unique id over recorded months.
    """
    
    template_name = 'analytics/list_by_month_year.html'
    model = PurchaseRecord
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        
        id_ = self.kwargs['driver_id_id']
        context = super(DriverSpendByMonth, self)\
            .get_context_data(**kwargs)
        
        # Django Way to Query on a Using SQL syntax.
        """
        This below given annotation will roughly translate
        to the query given:
            select DATE_FORMAT(dated, '%m-%Y') as Month_Year,
                sum(price*volume) as total_spent,
                count(*) as Record_Count
             from upload_purchaserecord
                    where driver_id_id=1
            group by DATE_FORMAT(dated, '%m-%Y');
        """
        purchase_record = PurchaseRecord\
            .objects\
            .filter(driver_id_id=id_) \
            .select_related('fuel_type_id')\
            .annotate(month=ExtractMonth('dated'),
                      year=ExtractYear('dated'),) \
            .values('month', 'year') \
            .annotate(total=Count('id'))\
            .annotate(record_count=Count('id'),
                      total_spent=Sum(F('price') * F('volume'))) \
            .values('month', 'year',
                    'total_spent', 'record_count',
                    'fuel_type__name')\
            .order_by('month', 'year', 'fuel_type')
        
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
    """
    FuelSpendView
        This view handles the landing page for Fuel Views
        The redirect fuel views are as:
            1. All Fuel Records
            2. Fuel Spend By Month
    """
    
    template_name = 'analytics/ctemplate.html'
    model = PurchaseRecord

    def get(self, request, **kwargs):
        form = FuelSpendForm()
        return render(request, self.template_name,
                      {'form': form})
    
    def post(self, request, **kwargs):
        by_time = request.POST.get('by_time')
        fuel = request.POST.get('fuel_spend')
        
        print(request.POST)
    
        if by_time == '0':
            return redirect('/trends/fuel/' + str(fuel))
    
        else:
            return redirect('/trends/fuel/total/month/' + str(fuel))
        
        
class FuelSpendDetails(ListView):

    template_name = 'analytics/list_all_records_template.html'
    model = PurchaseRecord
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = dict()
        fuel_id = self.kwargs.get('fuel_id')
        driver = DriverDetails.objects
        purchase_record = PurchaseRecord.objects\
            .filter(fuel_type=fuel_id) \
            .annotate(spent=F('price') * F('volume')) \
            .values('dated', 'volume',
                    'price', 'spent',
                    'driver_id__name'
                    )\
            .order_by('dated', 'driver_id')
        
        paginator = Paginator(purchase_record, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            page_by = paginator.page(page)

        except PageNotAnInteger:
            page_by = paginator.page(1)

        except EmptyPage:
            page_by = paginator.page(paginator.num_pages)

        context['fuel'] = FuelType.objects.get(fuel_id=fuel_id).name
        context['purchase_record'] = page_by

        return context
        
        
class FuelSpendByMonth(ListView):
    template_name = 'analytics/list_by_month_year.html'
    model = PurchaseRecord
    paginate_by = 15

    def get_context_data(self, **kwargs):
    
        fuel_id = self.kwargs.get('fuel_id')
        
        context = super(FuelSpendByMonth, self) \
            .get_context_data(**kwargs)
    
        # Django Way to Query on a Using SQL syntax.
        """
         This below given annotation will roughly translate
         to the query given:
         select
            sum(price*volume) as total_spent,
            DATE_FORMAT(dated, '%m') as Month,
            DATE_FORMAT(dated, '%Y') as Year,
            count(*) as record_count
         from upload_purchaserecord
            where fuel_type_id=id_
         group by DATE_FORMAT(dated, '%m'),
                  DATE_FORMAT(dated, '%Y');
        """
        
        purchase_record = PurchaseRecord.objects\
            .filter(fuel_type_id=fuel_id) \
            .annotate(month=ExtractMonth('dated'),
                      year=ExtractYear('dated'), ) \
            .values('month', 'year') \
            .annotate(total=Count('id')) \
            .annotate(record_count=Count('*'),
                      total_spent=Sum(F('price') * F('volume'))) \
            .values('month', 'year',
                    'total_spent', 'record_count',
                    'driver_id__name') \
            .order_by('month', 'year', 'driver_id__name')
    
        paginator = Paginator(purchase_record, self.paginate_by)
        page = self.request.GET.get('page')
    
        try:
            page_by = paginator.page(page)
    
        except PageNotAnInteger:
            page_by = paginator.page(1)
    
        except EmptyPage:
            page_by = paginator.page(paginator.num_pages)
    
        context['fuel'] = FuelType.objects.get(fuel_id=fuel_id).name
        context['purchase_record'] = page_by
    
        return context


#TODO: Add Spend URL & View By Year for Fuel
# Example 1: /trends/fuel/year/2019/month/08/
# The above must extract records for 08-2019
# Example 2: /trends/fuel/year/2019
# The above must extract all records by month for year 2019
    

class TotalSpendView(TemplateView):
    template_name = 'analytics/totalspend.html'


class AcrossSpendView(TemplateView):
    template_name = 'analytics/across.html'
