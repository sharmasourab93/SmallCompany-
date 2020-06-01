from django.db import models
  

DATE_INPUT_FORMATS = ['%Y-%m-%d']


class DriverDetails(models.Model):
    """
        Entries need to be made pre-requisite
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    registered_on = models.DateField()
    serial_id = models.CharField(unique=True, max_length=7)
    
    def __str__(self):
        return u'{0} -- {1}'.format(self.serial_id, self.name)


class FuelType(models.Model):
    """
        Pre-requisite entries need to be made.
    """
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
        return self.name + ' ' + str(self.fuel_id)


class FuelPrice(models.Model):

    fuel_name = models.ForeignKey(FuelType,
                                  on_delete=models.CASCADE,
                                  max_length=16)
    priced_date = models.DateField()
    price = models.DecimalField(max_digits=5,
                                decimal_places=2)
    
    def __str__(self):
        return self.fuel_name.name + ' ' + str(self.priced_date) + ' ' + str(self.price)


class PurchaseRecord(models.Model):
    """
        To be inserted on the front end.
    """
    
    id = models.AutoField(primary_key=True)
    fuel_type = models.ForeignKey(FuelType,
                                  on_delete=models.CASCADE,)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    volume = models.DecimalField(max_digits=5, decimal_places=2)
    driver_id = models.ForeignKey(DriverDetails,
                                  on_delete=models.CASCADE,)
    dated = models.DateField()
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
         return "{0}--{1}--{2}--{3}".format(self.driver_id, self.dated,
                                    self.price, self.volume)
    

class Document(models.Model):
    
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='upload/static/uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)