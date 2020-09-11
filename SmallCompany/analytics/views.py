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
from .forms import SpendByTimeForm

# Importing Logger and other python core modules.
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import logging
from re import sub


logger = logging.getLogger(__name__)


# 1. URL Route to Analytics Landing Page
class LandingView(TemplateView):
    """Landing View For Analytics Section"""
    template_name = 'analytics/analytics.html'
    

# 2. Driver Base View
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
        

# 2.a. Driver Spend Details
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


# 2.b. Total Driver Spend By Month
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


# 3. Fuel Spend View
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
    
        if by_time == '0':
            return redirect('/trends/fuel/' + str(fuel))
    
        else:
            return redirect('/trends/fuel/total/month/' + str(fuel))
        

# 3.a. Fuel Spend Details
class FuelSpendDetails(ListView):

    template_name = 'analytics/list_all_records_template.html'
    model = PurchaseRecord
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = dict()
        fuel_id = self.kwargs.get('fuel_id')
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
        

# 3.b. Fuel Spend By Fuel Type
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
    

# 4. Total Spend Across All times.
class TotalSpendView(ListView):
    template_name = 'analytics/list_by_month_year.html'
    model = PurchaseRecord
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        #context = super(TotalSpendView, self).__init__(**kwargs)
        context = dict()
        """
         This below given annotation will roughly translate
         to the query given:
         select d.name,
                sum(c.price * c.volume)as total_spent,
                DATE_FORMAT(c.dated, '%m-%Y') as dated,
                c.fuel_type_id as fuel_name
         from upload_purchaserecord c
         inner join  upload_driverdetails d on
            d.id = c.driver_id_id
         group by DATE_FORMAT(c.dated, '%m-%Y'),
                  c.fuel_type_id;
        """
        
        purchase_record = PurchaseRecord.objects \
            .annotate(month=ExtractMonth('dated'),
                      year=ExtractYear('dated'), ) \
            .values('month', 'year') \
            .annotate(total=Count('id')) \
            .annotate(total_spent=Sum(F('price') * F('volume'))) \
            .values('month', 'year',
                    'total_spent',
                    'driver_id__name',
                    'fuel_type__name') \
            
        summary = purchase_record.aggregate(sum=Sum('total_spent'))
        purchase_record = purchase_record.order_by('month', 'year', 'driver_id__name')
        
        context['total'] = purchase_record
        context['purchase_record'] = object
        context['sum'] = summary['sum']
        
        return context
    

# 5. Spend Specific to selected Time - Year and/or Month
class TotalSpendSpecific(TemplateView):
    """
    Total Spend Specific View
        This View redirects to Year and Month Specific URL
        on a post request.
    """
    
    template_name = 'analytics/ctemplate.html'
    form = SpendByTimeForm()
    context = dict()
    
    def get(self, request, *args, **kwargs):
        
        self.context['form'] = self.form
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        by_year = sub(r'[\(\)\,]', '', str(request.POST.get('year')))
        by_month = sub(r'[\(\)\,]', '', str(request.POST.get('month')))
        
        if by_month:
            return redirect('year/{0}/month/{1}'
                            .format(by_year, by_month))
        
        else:
            return redirect('year/{0}'.format(by_year))
        

# 5.a. & 5.b. Total Spent In a Specific Year or Month
class TotalSpendTimeSpecific(ListView):
    
    template_name = 'analytics/list_by_month_year.html'
    model = PurchaseRecord
    
    def get_context_data(self, **kwargs):
        context = dict()
        context['purchase_record'] = object
        by_year = self.kwargs['year']
        
        try:
            by_month = self.kwargs['month']
            self.template_name = \
                'analytics/list_all_records_template.html'

            # Django ORM(Query) to extract data for
            # a specific year and month.
            purchase_record = PurchaseRecord.objects\
                .annotate(year=ExtractYear('dated'),
                          month=ExtractMonth('dated'))\
                .values('year', 'month')\
                .annotate(total=Count('id'))\
                .filter(month=by_month, year=by_year) \
                .annotate(spent=F('price') * F('volume')) \
                
            
            summary = purchase_record.aggregate(sum=Sum('spent'))
            purchase_record = purchase_record\
                .values('dated', 'price',
                        'volume', 'spent',
                        'driver_id__name',
                        'fuel_type__name') \
                .order_by('dated', 'fuel_type__name')
            
            context['detail'] = object
            context['month'] = by_month
            context['year'] = by_year
            context['purchase_record'] = purchase_record
            context['sum'] = summary['sum']
            
            return context
            
        except KeyError:
            
            # Django ORM(Query) to extract data for a specific year
            total = PurchaseRecord.objects\
                .annotate(year=ExtractYear('dated'),
                          month=ExtractMonth('dated')) \
                .values('year', 'month')\
                .annotate(total=Count('id'))\
                .filter(year=by_year) \
                .annotate(total_spent=Sum(F('price') * F('volume'))) \
                .values('driver_id__name',
                        'fuel_type__name',
                        'month',
                        'year',
                        'total_spent') \
                .order_by('month', 'year', 'driver_id')
    
            summary = total.aggregate(sum=Sum('total_spent'))
    
            context['detail'] = object
            context['year'] = by_year
            context['total'] = total
            context['sum'] = summary['sum']
    
            return context
        

# 6. View Specific to Matplotlib
#TODO: Add Matplotlib component.
class AcrossSpendView(TemplateView):
    template_name = 'analytics/across.html'
