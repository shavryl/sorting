from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.




class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=100)
    lastname = models.CharField( blank=False, max_length=100)
    city = models.CharField( blank=True, max_length=100)
    country = models.CharField( blank=True, max_length=100)
    phonenumber = models.CharField(blank=False, null=True, max_length=20)
    email = models.EmailField(blank=False, max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_addition = models.DateField(auto_now=True, editable=False, null=True)



class MyVeroKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verokey = models.CharField(blank=True, max_length=110)

