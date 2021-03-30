from django.shortcuts import render
from django.http import HttpResponse
from hospital.models import hosp_inv, hosp_req, supp_storage, supp_inv
import datetime
import time
from django.shortcuts import redirect
import random

# def logout_request(request):
#     logout(request)
#     messages.info(request, "Logged out successfully!")
#     return redirect("main:homepage")

n_items = 20

hosps = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
]

supps = [
    'A', 'B', 'E',
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

def fill_hosp_inv(request):
    for i in range(n_items):
        new_hosp_inv = random_hosp_inv()
        try:
            new_hosp_inv.save()
        except Exception:
            pass
    
    return redirect('/')

def homepage(request):
    # return HttpResponse("<h1> HELLO </h1>")
    # return render(request, 'hospital/home.html')
    return render(request, 'hospital/home.html')


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
    # Drugs least commonly prescribed at a hospital

    counts = dict()
    start = time.time()
    for i in range(8):
        date = datetime.date.today() - datetime.timedelta(days=i)
        objs = hosp_req.objects.filter(hosp_name=hospital, date=date)

        for obj in objs:
            if obj.itemname not in counts.keys():
                counts[obj.itemname] = obj.quantity
            else:
                counts[obj.itemname]+=obj.quantity
    
    end = time.time()-start


    counts = dict(sorted(counts.items(), key=lambda item: item[1]))

    print(counts)

    return render(request, 'hospital/metric_01.html', context={"objs": counts, "hospital": hospital, "exectime": end})


def metric_02_viewpage(request, hospital='A'):
    # Drugs most commonly prescribed at a hospital

    counts = dict()
    start = time.time()
    for i in range(8):
        date = datetime.date.today() - datetime.timedelta(days=i)
        objs = hosp_req.objects.filter(hosp_name=hospital, date=date)

        for obj in objs:
            if obj.itemname not in counts.keys():
                counts[obj.itemname] = obj.quantity
            else:
                counts[obj.itemname]+=obj.quantity
    
    end = time.time()-start


    counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    print(counts)

    return render(request, 'hospital/metric_02.html', context={"objs": counts, "hospital": hospital, "exectime": end})

def reset_supp_storage(request):
    objs = supp_storage.objects.all()
    for obj in objs:
        obj.occupied=0
        obj.save()
    
    return redirect('/')

def random_supp_inv():
    new_supp_inv= supp_inv()
    new_supp_inv.supp_name = random.choice(supps)
    print(new_supp_inv.supp_name)
    storage = supp_storage.objects.get(supp_name=new_supp_inv.supp_name)
    new_supp_inv.itemname = random.choice(drugnames)
    quantity  = random.randint(10, 100)
    maxi = storage.maximum-storage.occupied
    if(maxi == 0):
        return None
    while quantity > maxi:
        quantity  = random.randint(1, maxi)
    
    new_supp_inv.quantity = quantity

    new_supp_inv.date = datetime.date.today() - datetime.timedelta(days=random.randint(0,8))
    return new_supp_inv

def fill_supp_inv(request):
    counts = 0
    for i in range(n_items):
        new_supp_inv = random_supp_inv()
        print(new_supp_inv)
        try:
            new_supp_inv.save()
            storage = supp_storage.objects.get(supp_name=new_supp_inv.supp_name)
            storage.occupied += new_supp_inv.quantity
            storage.save()
        except Exception:
            print("Triggered")
            count+=1
            pass
    print("Count ", counts)

    return redirect('/')

def metric_03_viewpage(request, supplier = 'E'):
    # Drugs most commonly in stock at a supplier

    counts = dict()
    objs = supp_inv.objects.filter(sold=False)
    start = time.time()
    
    for obj in objs:
        if obj.itemname not in counts.keys():
            counts[obj.itemname] = obj.quantity
        else:
            counts[obj.itemname]+=obj.quantity
    
    end = time.time()-start


    counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    print(counts)

    return render(request, 'hospital/metric_03.html', context={"objs": counts, "supplier": supplier, "exectime": end})

def metric_04_viewpage(request, supplier = 'E'):
    # Drugs least moved at a supplier

    counts = dict()
    objs = supp_inv.objects.filter(sold=True)
    start = time.time()
    
    for obj in objs:
        if obj.itemname not in counts.keys():
            counts[obj.itemname] = obj.quantity
        else:
            counts[obj.itemname]+=obj.quantity
    
    end = time.time()-start


    counts = dict(sorted(counts.items(), key=lambda item: item[1]))

    print(counts)

    return render(request, 'hospital/metric_04.html', context={"objs": counts, "supplier": supplier, "exectime": end})