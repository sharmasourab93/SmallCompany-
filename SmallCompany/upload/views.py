from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from .models import FuelPrice, FuelType
from .models import PurchaseRecord, DriverDetails
from .forms import UpdateForm, UploadForm
import os


class LandingView(TemplateView):
    
    template_name = 'upload/landingpage.html'
    
    def get(self, request, **kwargs):
        
        return render(request, self.template_name)


class HomeView(TemplateView):
    
    template_name = 'upload/home.html'
    model = PurchaseRecord
    
    def get(self, request, **kwargs):
    
        form = UpdateForm()
        
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, **kwargs):
        
        form = UpdateForm(request.POST)
        items = list()
        
        if form.is_valid():
            
            """
                Looking for fuel in the form
            """
            
            fuel = form.cleaned_data['fuel']
            query_fuel = None
            
            try:
                query_fuel = FuelType.objects.filter(fuel_id=fuel)[0]
                items.append(query_fuel)
                
            except ObjectDoesNotExist:
                
                query_fuel = None
                text = "Issues with Fuel Type"
                
                return render(request,
                              self.template_name,
                              {'form': form, 'text': text})
            
            """
                Looking for date of purchase in the form
            """
            
            dated = form.cleaned_data['date']
            price = 0.00
            
            try:
                dated_bool = date_compare(dated)
                items.append(dated)
                
                price = FuelPrice.objects.filter(fuel_name=query_fuel, priced_date=dated)
                f_price = float(price[0].price)
                
                items.append(f_price)
                
            except DateBeyondCurrentException:
                
                text = "Given date is ahead the current date"
                
                return render(request,
                              self.template_name,
                              {'form': form, 'text': text})
            
            """
                Get Volume in decimal format
            """
            
            try:
                volume = form.cleaned_data['volume']
                volume = float(volume)
                items.append(volume)
                
            except ValueError:
                text = "Given value is not a float value"
    
                return render(request,
                              self.template_name,
                              {'form': form, 'text': text})
            
            """
                Get Driver Id and verify if the object exists or not
            """
            
            try:
                
                driver_id = form.cleaned_data['driver_id']
                driver_obj = DriverDetails.objects.filter(serial_id=driver_id)[0]
                items.append(driver_obj)
                
            except ObjectDoesNotExist:
                text = "Giver Driver Id doesn't exist in the records"
                
                return render(request,
                              self.template_name,
                              {'form': form, 'text': text})
            
            keys = ['fuel_type', 'dated', 'price', 'volume', 'driver_id']
            
            m = self.model(fuel_type=items[0], dated=items[1],
                           price=items[2], volume=items[3],
                           driver_id=items[4]).save()
            
            text = "All entries are valid. Updated Successfully!"
            
            return render(request,
                          self.template_name,
                          {'form': form, 'text': text})
        
        else:
            
            return render(request,
                          self.template_name,
                          {'form': form})
    

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
        
        if date_1 <= date_2:
            return True
        
        else:
            
            raise DateBeyondCurrentException(date)


class UploadView(TemplateView):
    
    template_name = 'upload/upload_file.html'
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


class DateBeyondCurrentException(Exception):
    
    def __init__(self, date):
        Exception.__init__(self)
        self.date = date
