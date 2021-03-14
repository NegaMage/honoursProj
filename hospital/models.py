from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

# Create your models here.

hospital_names = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
]

class hosp_inv(models.Model):
    """ Maintain a running inventory of stock at hospital.
        Updated automatically when hosp_req is changed."""
    itemname = models.CharField(max_length=200)
    quantity = models.IntegerField()
    hosp_name = models.CharField(choices=hospital_names, max_length=10)

    def __str__(self):
        return self.itemname

class hosp_req(models.Model):
    """ Used in day-to-day of hospital. Managers keep track of what
        has been consumed, and corresponding edits happen to hosp_inv."""
    itemname = models.CharField(max_length=200)
    quantity = models.IntegerField()
    hosp_name = models.CharField(choices=hospital_names, max_length=10)
    date = models.DateField(verbose_name="Date of change")

    def __str__(self):
        return self.itemname

class hosp_est(models.Model):
    """ Analytics table, keeps track of what has been consumed in what month."""
    itemname = models.CharField(max_length=200)
    quantity = models.IntegerField()
    hosp_name = models.CharField(choices=hospital_names, max_length=10)
    date = models.DateField(verbose_name="Date of record")

    def __str__(self):
        return self.itemname

    def clean(self):
        hosp_inv_item = hosp_inv(itemname=self.itemname, hosp_name=self.hosp_name)
        if(hosp_inv_item.quantity + self.quantity <0):
            raise ValidationError(gettext_lazy("Net inventory is negative after operation."))
        

class hosp_emp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.CharField(choices=hospital_names, max_length=10, default="A")

    def __str__(self):
        return self.user.username