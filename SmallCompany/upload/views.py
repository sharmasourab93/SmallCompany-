# Imports related to Contrib/Auth.
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

# Imports for exception handling
from django.core.exceptions import ObjectDoesNotExist

# Imports related to URL
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden

# Template/View Import
from django.views.generic import TemplateView

# Imports related to Models.
from .models import FuelPrice, FuelType
from .models import PurchaseRecord, DriverDetails

# Imports from forms.
from .forms import PurchaseUpdateForm, UploadForm, LoginForm
from .forms import PriceUpdateForm, DriverEnrollmentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

# Core Python Imports
import os
import logging


logger = logging.getLogger(__name__)


# 1. Sign Up - Register a User
def sign_up(request):
    # logger.info('SignUp for {0}'.format(request.user))
    context = {}
    form = UserCreationForm(request.POST or None)
    
    if request.user.is_active and request.user.is_authenticated:
        # logger.warning('Access Forbidden for {0}'.format(request.user))
        return HttpResponseForbidden()
    
    if request.method == "POST":
        # logger.debug('POST received. Redirecting to Filling')
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/filldetails/')
    
    context['form'] = form
    return render(request, 'registration/signup.html', context)


# 2. Login a user
def login_user(request):
    context = dict()
    form = LoginForm()
    another_form = UserCreationForm(request.POST or None)
    
    if request.user.is_active and request.user.is_authenticated:
        return HttpResponseForbidden()
    
    if request.method == 'GET':
        context = {'form': form}
        return render(request, 'registration/login.html', context)
    
    else:
        user = form.login(request)
        
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'mainapp/index.html', {'user':user})
        
        invalid = {'message':"Invalid Login", 'form':form}
        return render(request, "registration/login.html", invalid)


# 4. Logout a user
@login_required
def logout(request):
    logout(request)
    return render(request, "registration/logout.html")


# 5. Password Change Not a priority
@login_required
def password_change(request):
    if request.method == 'POST' and request.user.is_active:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your Password was successfully updated!")
            return redirect('/accounts/login/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'registration/password.html', {'form':form})


# 05. Landing View
class LandingView(TemplateView):
    
    template_name = 'upload/landingpage.html'
    
    def get(self, request, **kwargs):
        
        return render(request, self.template_name)


# 06. Single Record Update, Purchase Record Update
class PurchaseUpdate(TemplateView):
    template_name = 'upload/base_template.html'
    form = PurchaseUpdateForm()
    
    def get(self, request, **kwargs):
        return render(request,
                      self.template_name,
                      {'form':self.form})
    
    def post(self, request, **kwargs):
        object = request.POST
        price = object['price']
        volume = object['volume']
        dated = object['dated']
        fuel_type = FuelType.objects.get(fuel_id=object['fuel_type']).fuel_id
        driver_id = DriverDetails.objects.get(id=object['driver_id']).id
        
        purchase_update = PurchaseRecord(fuel_type_id=fuel_type,
                                         driver_id_id=driver_id,
                                         dated=dated,
                                         price=price,
                                         volume=volume)
        purchase_update.save()
        
        return render(request,
                      self.template_name,
                      {
                          'form':self.form,
                          'context':"Purchase Update done!"
                          })


# 07. Bulk Record Update
class UploadView(TemplateView):
    
    template_name = 'upload/base_template.html'
    model = PurchaseRecord
    location = 'upload/static/uploads'
    mal_list = []

    def get(self, request, **kwargs):
    
        form = UploadForm()
    
        return render(request, self.template_name, {'form': form})
    
    def handle_uploaded_file(self, up_file):
        # up = list(up_file['document'])
        file_pointer = os.path.join(self.location, up_file.name)
        fd = open(file_pointer, 'wb')
        for chunk in up_file.chunks():
            fd.write(chunk)
            
        fd.close()
        
    def insert_into_model(self, sent_list):
        items = list()
        fuel_type, date, volume, driver_id = sent_list
        
        try:
            query_fuel = FuelType.objects.filter(name=fuel_type)[0]
            items.append(query_fuel)

            dated_bool = date_compare(date)
            items.append(date)
            
            price = FuelPrice.objects.filter(fuel_name=query_fuel,
                                             priced_date=items[1])[0]
            items.append(price.price)

            volume = float(volume)
            items.append(volume)
            
            driver_obj = DriverDetails.objects.filter(serial_id=driver_id)[0]
            items.append(driver_obj)
            
            m = self.model(fuel_type=items[0], dated=items[1],
                           price=items[2], volume=items[3],
                           driver_id=items[4]
                           ).save()
            
            return True

        except ObjectDoesNotExist:
            
            self.mal_list.append(sent_list)
            return False
            
        except DateBeyondCurrentException:

            self.mal_list.append(sent_list)
            return False
        
        except ValueError:
            sent_list.append('valueError')
            self.mal_list.append(sent_list)
            return False
        
        except IndexError:
            return True
        
    def post(self, request, **kwargs):
        
        form = UploadForm(request.POST, request.FILES)
        self.mal_list.clear()
        
        if form.is_multipart():
            
            self.handle_uploaded_file(request.FILES['document'])
            file_name = request.FILES['document'].name
            
            file_name = os.path.join(self.location, file_name)
            file_open = open(file_name, 'r+')
            
            for i in file_open.readlines():
                
                j = i.replace('\n', '').split(', ')
                
                if self.insert_into_model(j) is True:
                    
                    # Logging can be done here
                    # to verify if the upload
                    # is successful or not
                    continue
            
            if len(self.mal_list) == 0:
                
                text = "File Uploaded successfully."
                
                return render(request,
                              self.template_name,
                              {'form': form, 'text': text})
            
            else:
                
                text = "File Uploaded Successfully."
                text += "Some Invalid records found."
                
                record = str(self.mal_list)
                record += str(request.FILES['document'])
                return render(request,
                              self.template_name,
                              {'form': form,
                               'text': text,
                               'records': record})
                
        else:
            
            text = "Issues with uploading of file."

            return render(request, self.template_name,
                          {'form': form, 'text': text})


# 08. Price Update Form
class PriceUpdation(TemplateView):
    template_name = "upload/base_template.html"
    
    def get(self, request, **kwargs):
        form = PriceUpdateForm()
        return render(request,
                      self.template_name,
                      {'form': form})
    
    def post(self, request, **kwargs):
        
        form = PriceUpdateForm()
        fuel = request.POST.get('fuel')
        fuel = FuelType.objects.get(fuel_id=fuel)
        date = request.POST.get('date')
        price = request.POST.get('price')
        items = FuelPrice(fuel_name=fuel, priced_date=date, price=price)
        items.save()
        return render(request,
                      self.template_name,
                      {'context': "saved!(Y)"}
                      )
            

# 09. Driver Enrollment Form View
class DriverEnrollment(TemplateView):
    template_name = "upload/base_template.html"
    form = DriverEnrollmentForm()
    
    def get(self, request, **kwargs):
        
        return render(request,
                      self.template_name,
                      {'form': self.form})
    
    def post(self, request, **kwargs):
            
            object = request.POST
            name, address = object.get('name'), object.get('address')
            registered_on = object.get('registered_on')
            serial_id = object.get('serial_id')
            
            driver_ = DriverDetails(name=name,
                                    address=address,
                                    registered_on=registered_on,
                                    serial_id=serial_id)
            driver_.save()
            
            success_ = "{0}'s record saved Successfully!".format(name)
            return render(request,
                          self.template_name,
                          {'context': success_,
                           'form': self.form})


# Date Exception Utility
class DateBeyondCurrentException(Exception):
    
    def __init__(self, date):
        Exception.__init__(self)
        self.date = date


# Date Compare Method, utilized in 07. Bulk Upload
def date_compare(date):

    """
     Compares if the given date is bigger than the
     current date.
    :param date:
    :return: True or DateBeyondCurrentException
    """
    import datetime
    y1, m1, d1 = [int(x) for x in str(date).split('-')]
    y2, m2, d2 = [int(x) for x in
                  str(datetime.date.today()).split('-')]

    date_1 = datetime.date(y1, m1, d1)
    date_2 = datetime.date(y2, m2, d2)

    if date_1<=date_2:
        return True

    else:
    
        raise DateBeyondCurrentException(date)
