from django.db import models
from django.utils import timezone
# Create your models here



class EntryRequest(models.Model):
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    bushperc = models.DecimalField(max_digits=5,decimal_places=2)
    leafperc = models.DecimalField(max_digits=5,decimal_places=2)
    Q = models.CharField(max_length=200)
    height = models.CharField(max_length=200)
    stability_class = models.CharField(max_length=200)
    wind = models.DecimalField(max_digits=5,decimal_places=2)
    rain = models.DecimalField(max_digits=5,decimal_places=2)
    RH =  models.DecimalField(max_digits=5,decimal_places=2)
    irradiance = models.DecimalField(max_digits=5,decimal_places=2)
    location = models.CharField(max_length=200)
    maxdis = models.CharField(max_length=200,default=0)

    added = models.DateTimeField(default=timezone.now())#auto_now_add=True)
