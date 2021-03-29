
from django_seed import Seed
import random
seeder = Seed.seeder()
from pathlib import Path

DJANGO_SETTINGS_MODULE = Path(__file__).resolve().parent.parent

hospital_names = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G',
]

ITEMNAME_CHOICES = [
    'penicillin', 
    'chlordiazepram',
    'wakalixes',
    'tylenol',
    'mortein',
    'vicks,',
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

from hospital.models import hosp_inv
seeder.add_entity(hosp_inv, 50, {
    'hosp_name' : lambda x: random.choice(hospital_names),
    'itemname' : lambda x: random.choice(ITEMNAME_CHOICES),
    'quantity'  : lambda x: random.randint(100, 10000),

})


inserted_pks = seeder.execute()


