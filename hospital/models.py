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
    ('H', 'H'),
    ('I', 'I'),
    ('J', 'J'),
]

class hosp_inv(models.Model):
    """ Maintain a running inventory of stock at hospital.
        Updated automatically when hosp_req is changed."""
    itemname = models.CharField(max_length=200)
    quantity = models.IntegerField()
    hosp_name = models.CharField(choices=hospital_names, max_length=10)

    def __str__(self):
        return "{}, {}, {}".format(self.itemname, self.hosp_name, self.quantity)

    class Meta:
        unique_together = ("itemname", "hosp_name")

class hosp_req(models.Model):
    """ Used in day-to-day of hospital. Managers keep track of what
        has been consumed, and corresponding edits happen to hosp_inv."""
    itemname = models.CharField(max_length=200)
    quantity = models.IntegerField()
    hosp_name = models.CharField(choices=hospital_names, max_length=10)
    date = models.DateField(verbose_name="Date of change")

    def __str__(self):
        return "{}, {}, {}".format(self.itemname, self.hosp_name, self.quantity)

    class Meta:
        unique_together = ("itemname", "hosp_name", "date")


supplier_names = [
    ('A', 'A'),
    ('B', 'B'),
    ('E', 'E'),
]

class supp_storage(models.Model):
    """ Keep a record of inventory space of each supplier. This data isn't shown outside, but secret to each supplier, and modifiable in the portal. """
    supp_name = models.CharField(choices=supplier_names, max_length=10, primary_key=True)
    maximum = models.IntegerField()
    occupied = models.IntegerField()
    

    def __str__(self):
        return "{}, {}".format(self.supp_name, self.maximum)
    
    def clean(self):
        if(self.occupied > self.maximum):
            raise ValidationError(gettext_lazy("Storage can't be more than maximum capacity."))


class supp_inv(models.Model):
    """ The explicit contents of each suppliers' inventory. Total quantity keeps getting updated in the other table. """
    supp_name = models.CharField(choices=supplier_names, max_length=10)
    itemname = models.CharField(max_length=200)
    quantity = models.IntegerField()
    sold = models.BooleanField(default=False)

    date = models.DateField(verbose_name="Inventory date")


    def __str__(self):
        return "{}, {}".format(self.supp_name, self.itemname)
    
    # def delete(self):
    #     storage = supp_storage.objects.get(supp_name=self.supp_name)
    #     storage.occuped -= self.quantity
    #     self.delete()

manuf_names = [
    ('D', 'D'),
    ('G', 'G'),
]

class manuf_making(models.Model):
    man_name = models.CharField(max_length=10, choices=manuf_names)
    itemname = itemname = models.CharField(max_length=200)
    quantity = models.IntegerField()
    date_of_production = models.DateField()
    sold = models.BooleanField(default=False)

