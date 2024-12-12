from django.db import models
from users.models import User
from datetime import timedelta



class Flight(models.Model):
    image = models.ImageField(upload_to='flight_images/')
    airline = models.ForeignKey('web.Airlines', on_delete=models.CASCADE)
    flight_numbers = models.CharField(max_length=100)
    departure_time = models.TimeField()
    departure_code = models.CharField(max_length=10)
    duration = models.DurationField(default=timedelta(hours=2)) 
    stops = models.CharField(max_length=50) 
    arrival_time = models.TimeField()
    arrival_code = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    
    class Meta:
        db_table = "flight"
        verbose_name = "flight"
        verbose_name_plural = "flights"
        ordering = ["-id"]


    def __str__(self):
        return self.airline.name
    


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "customer_customer"
        verbose_name = "customer"
        verbose_name_plural = "customers"
        ordering = ["-id"]

    def __str__(self):
        return self.user.email

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories')
    
    
    
    class meta:
           db_table = "category"
           verbose_name = "category"
           verbose_name_plural = "categories"
           ordering = ['-id']
    
    
    def __str__(self):
          return self.name
   
class Slider(models.Model):
    name =  models.CharField(max_length=255)
    image = models.ImageField(upload_to='slider')
    
    
    class meta:
        db_table = "slider"
        verbose_name = "slider"
        verbose_name_plural = "sliders"
        ordering = ['-id']
    
    
    def __str__(self):
        return self.name
class Airlines(models.Model):
    name = models.CharField(max_length=255)
    
    
    class meta:
        db_table = "Airlines"
        verbose_name = "Airlines"
        verbose_name_plural = "Airlineses"
        ordering = ['-id']
    
    
    def __str__(self):
        return self.name
    

class Train(models.Model):
    image = models.ImageField(upload_to='train_images/')
    trains = models.ForeignKey('web.Trains', on_delete=models.CASCADE)
    train_numbers = models.CharField(max_length=100)
    departure_time = models.TimeField()
    departure_code = models.CharField(max_length=10)
    duration = models.DurationField(default=timedelta(hours=1)) 
    stops = models.CharField(max_length=50) 
    arrival_time = models.TimeField()
    arrival_code = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    
    class Meta:
        db_table = "train"
        verbose_name = "train"
        verbose_name_plural = "trains"
        ordering = ["-id"]


    def __str__(self):
        return self.trains.name
    
class Bus(models.Model):
    image = models.ImageField(upload_to='bus_images/')
    buses = models.ForeignKey('web.Buses', on_delete=models.CASCADE)
    bus_numbers = models.CharField(max_length=100)
    departure_time = models.TimeField()
    departure_code = models.CharField(max_length=10)
    duration = models.DurationField(default=timedelta(hours=1)) 
    stops = models.CharField(max_length=50) 
    arrival_time = models.TimeField()
    arrival_code = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    
    class Meta:
        db_table = "bus"
        verbose_name = "bus"
        verbose_name_plural = "buses"
        ordering = ["-id"]


    def __str__(self):
        return self.Buses.name
    
    
class Buses(models.Model):
    name = models.CharField(max_length=255) 
    
    class meta:
        db_table = "bus"
        verbose_name = "bus"
        verbose_name_plural = "buses"
        ordering = ['-id']
    
    
    def __str__(self):
        return self.name
    
    
class Trains(models.Model):
    name = models.CharField(max_length=255)
    class meta:
        db_table = "trains"
        verbose_name = "trains"
        verbose_name_plural = "trainses"
        ordering = ['-id'] 
    
    def __str__(self):
        return self.name
    
    
    
class Offer(models.Model):
    code = models.CharField(max_length=255)
    discount = models.FloatField()
    short_description = models.CharField(max_length=255)
    is_percentage = models.BooleanField()
    
    
    class Meta:
        db_table = "offer"
        verbose_name = "offer"
        verbose_name_plural = "offers"
        ordering = ["-id"]

    def __str__(self):
        return self.code
    
    
    
class FlightBill(models.Model):
    fligths = models.ForeignKey(Flight, on_delete=models.CASCADE)
    airline_name = models.CharField(max_length=255)
    flight_code = models.CharField(max_length=50)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.CharField(max_length=50)
    departure_airport = models.CharField(max_length=255)
    arrival_airport = models.CharField(max_length=255)
    baggage_allowance = models.CharField(max_length=50)
    cabin_baggage = models.CharField(max_length=50)
    check_in_baggage = models.CharField(max_length=50)
    terminal = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.flight_code} - {self.airline_name}"
    
    
class  CartBill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item_total = models.FloatField()
    offer_amount = models.FloatField()
    totel_amount = models.FloatField()
    tax_charge = models.FloatField()
    
    
    class Meta:
        db_table = "customer_cartbill"
        verbose_name = "cartbill"
        verbose_name_plural = "cartbills"
        ordering = ["-id"]

    def __str__(self):
        return self.customer.user.email
    
    
class BusDetail(models.Model):
    buses = models.ForeignKey(Bus, on_delete=models.CASCADE)
    bus_name = models.CharField(max_length=255)
    bus_code = models.CharField(max_length=50)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.CharField(max_length=50)
    departure_stop = models.CharField(max_length=255)
    arrival_stop = models.CharField(max_length=255)
    baggage_allowance = models.CharField(max_length=50)
    cabin_baggage = models.CharField(max_length=50)
    check_in_baggage = models.CharField(max_length=50)
    terminal = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.bus_code} - {self.bus_name}"
    
    
class TrainDetail(models.Model):
    trains = models.ForeignKey(Train, on_delete=models.CASCADE)
    train_name = models.CharField(max_length=255)
    train_code = models.CharField(max_length=50)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.CharField(max_length=50)
    departure_stop = models.CharField(max_length=255)
    arrival_stop = models.CharField(max_length=255)
    baggage_allowance = models.CharField(max_length=50)
    cabin_baggage = models.CharField(max_length=50)
    check_in_baggage = models.CharField(max_length=50)
    terminal = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.train_code} - {self.train_name}"
    
    
