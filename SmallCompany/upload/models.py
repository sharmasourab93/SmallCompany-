from django.db import models
  

class DriverDetails(models.Model):
    # User defined Entries are made to
    # define the Driver functionality.
    
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    registered_on = models.DateField()
    serial_id = models.CharField(unique=True, max_length=7)
    
    def __str__(self):
        return u'{0} -- {1}'.format(self.serial_id, self.name)


class FuelType(models.Model):
    # Pre-requisite entries were made.
    # Classified different fuels for which
    # prices can be accordingly calculated.
    
    fuel_id = models.AutoField(primary_key=True)
    FUEL_OPTIONS = (
        (1, 'CNG'),
        (2, 'PETROL'),
        (3, 'DIESEL'),
        (4, 'HYDROGEN'),
        (5, 'LIQUID NITROGEN'),
        (6, 'BIODIESEL')
        )
    name = models.CharField(unique=True,
                            choices=FUEL_OPTIONS,
                            max_length=16)
    
    def __str__(self):
        return self.name


class PurchaseRecord(models.Model):
    
    # Purchase Record Model,
    # Keeps tab on all the incurred expenses.
    
    # Id isn't needed, unless you want to
    # add more features to your id field.
    # id = models.AutoField(primary_key=True)
    fuel_type = models.ForeignKey(FuelType,
                                  on_delete=models.CASCADE,)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    volume = models.DecimalField(max_digits=5, decimal_places=2)
    driver_id = models.ForeignKey(DriverDetails,
                                  on_delete=models.CASCADE,)
    dated = models.DateField()
    created = models.DateTimeField(auto_now=True)
    
    # __str__ method defines how the
    # PurchaseRecord object will look like.
    def __str__(self):
         return "{0}--{1}--{2}--{3}"\
             .format(self.driver_id, self.dated,
                     self.price, self.volume)
    

class Document(models.Model):
    # Model to Keep tab on uploaded files.
    
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='upload/static/uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class FuelPrice(models.Model):
    # Fuel Price : Redundant model
    # Originally Inteded to use as a foreign key
    # for price field in Purchase record, but
    # wasn't implemented due to time constraint.
    # But nevertheless, will be too time consuming for
    # re-consituting the same into an already built setup.

    fuel_name = models.ForeignKey(FuelType,
                                  on_delete=models.CASCADE,
                                  max_length=16)
    priced_date = models.DateField()
    price = models.DecimalField(max_digits=5,
                                decimal_places=2)
