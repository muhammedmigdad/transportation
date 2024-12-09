from django.db import models
from users.models import User
from datetime import timedelta



class Flight(models.Model):
    image = models.ImageField(upload_to='flight_images/')
    airline = models.CharField(max_length=100)
    flight_numbers = models.CharField(max_length=100)
    departure_time = models.TimeField()
    departure_code = models.CharField(max_length=10)
    duration = models.DurationField(default=timedelta(hours=2)) 
    stops = models.CharField(max_length=50) 
    arrival_time = models.TimeField()
    arrival_code = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def discounted_price(self):
        return self.price - self.discount if self.discount else self.price

    def __str__(self):
        return self.airline
    
    class Meta:
        db_table = "flight"
        verbose_name = "flight"
        verbose_name_plural = "flights"
        ordering = ["-id"]


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
    name =  models.CharField(max_length=255)
    
    
    class meta:
        db_table = "Airlines"
        verbose_name = "Airlines"
        verbose_name_plural = "Airlineses"
        ordering = ['-id']
    
    
    def __str__(self):
        return self.name
    

    
