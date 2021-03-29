from django.shortcuts import render
from django.http import HttpResponse
from hospital.models import hosp_inv, hosp_req
import datetime
from django.shortcuts import redirect
import random

# def logout_request(request):
#     logout(request)
#     messages.info(request, "Logged out successfully!")
#     return redirect("main:homepage")

hosps = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G',
]

graph = {
    'A' : ['B', 'F', 'G'],
    'B' : ['A', 'C'],
    'C' : ['B', 'D'],
    'D' : ['C', 'E', 'G'],
    'E' : ['D', 'F'],
    'F' : ['A', 'E', 'G'],
    'G' : ['A', 'D', 'F'],
}

drugnames = [
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
    new_hosp_inv.hosp_name = random.choice(hosps)
    new_hosp_inv.itemname = random.choice(drugnames)
    new_hosp_inv.quantity  = random.randint(10, 100)

    return new_hosp_inv

n_attempts = 10

def fill_hosp_inv(request):
    for i in range(n_attempts):
        new_hosp_inv = random_hosp_inv()
        try:
            new_hosp_inv.save()
        except Exception:
            pass
    
    return redirect('/')

def homepage(request):
    # return HttpResponse("<h1> HELLO </h1>")
    # return render(request, 'hospital/home.html')
    return render(request, 'hospital/home.html', context={"objs": hosp_inv.objects.all()})


def clean_hosp_inv(request):
    date = datetime.date.today()

    for hosp in hosps:
        
        for drug in drugnames:
            temp = 0
            objs = hosp_inv.objects.filter(itemname=drug, hosp_name=hosp)
            for obj in objs:
                temp+=obj.quantity
            objs.delete()    

            prev = hosp_req.objects.filter(itemname=drug, hosp_name=hosp, date=date)
            
            if(temp>0):
                if(len(prev)==0):
                    h = hosp_req(itemname=drug, hosp_name=hosp, quantity=temp, date=date)
                    h.save()
                else:
                    
                    print(prev[0])
                    prev[0].quantity = temp
                    prev[0].save()
            else:
                pass

    return redirect('/')


def metric_01_viewpage(request, hospital='A'):
    # Drugs most commonly prescribed at a hospital

    counts = dict()

    for i in range(8):
        date = datetime.date.today() - datetime.timedelta(days=i)
        objs = hosp_req.objects.filter(hosp_name=hospital, date=date)

        for obj in objs:
            if obj.itemname not in counts.keys():
                counts[obj.itemname] = obj.quantity
            else:
                counts[obj.itemname]+=obj.quantity
        
    counts = dict(sorted(counts.items(), key=lambda item: item[1]))

    print(counts)

    return render(request, 'hospital/metric_01.html', context={"objs": counts, "hospital": hospital})