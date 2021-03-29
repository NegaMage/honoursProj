import random
from datetime import timedelta

from django.contrib.auth.models import User
from faker import Faker
from hospital.models import hosp_inv

fake = Faker()

hospital_names = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G',
]

n_attempts = 160

ITEMNAME_CHOICES = [
    'penicillin', 
    'chlordiazepram',
    'wakalixes',
    'tylenol',
    'mortein',
    'vicks',
    'cough syrup',
    'kratom',
    'kartoffel',
    'asparagus',
    'codeine',
    'novocaine',
    'lysergenic acid diethylamide',
    'insulin',
    'coca leaf extract',
]

def random_hosp_inv():
    new_hosp_inv= hosp_inv()
    new_hosp_inv.hosp_name = random.choice(hospital_names)
    new_hosp_inv.itemname = random.choice(ITEMNAME_CHOICES)
    new_hosp_inv.quantity  = random.randint(100, 10000)

    return new_hosp_inv
    
def fill_hosp_inv():
    for i in range(n_attempts):
        new_hosp_inv = random_hosp_inv()
        try:
            new_hosp_inv.save()
        except Exception:
            pass
        


