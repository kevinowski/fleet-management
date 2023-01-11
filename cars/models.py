from django.db import models
from django.utils.text import slugify 
from django.core.exceptions import ValidationError

# Create your models here.


class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    reg_plate = models.CharField(max_length=50, unique=True, )
    mileage = models.IntegerField()
    last_service_mileage = models.IntegerField(default=mileage)
    service_interval = models.IntegerField()
    slug = models.SlugField(blank=True, unique=True)
    
    
    def get_car(self):
        return f"{self.brand} {self.model}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.get_car())
        super(Car, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.get_car()


class Refuel(models.Model):
    class Meta:
        ordering = ['-mileage']

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    mileage = models.IntegerField(null=True)
    liters = models.IntegerField(null=True)
    city = models.CharField(max_length=70, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    

    def __str__(self):
        return str(self.car)
    

class Service(models.Model):
    class Meta:
        ordering = ["-date_reported"]

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    mileage = models.IntegerField(null=True)
    service_type = models.CharField(max_length=40)
    description = models.TextField(max_length=300, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    date_fixed = models.DateField(null=True)

    def __str__(self):
        return str(self.car)
