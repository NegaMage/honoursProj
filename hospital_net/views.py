from django.shortcuts import render
from django.http import HttpResponse
from hospital.models import hosp_inv, hosp_req, supp_storage, supp_inv, manuf_making
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

manufs = [
    'D', 'G',
]

graph = {
    'A' : ['B', 'F', 'G'],
    'B' : ['A', 'C', 'H'],
    'C' : ['B', 'D', 'I'],
    'D' : ['C', 'E', 'G'],
    'E' : ['D', 'F'],
    'F' : ['A', 'E', 'G'],
    'G' : ['A', 'D', 'F'],
    'H' : ['B', 'I'],
    'I' : ['C', 'H', 'J'],
    'J' : ['D', 'I'],
}

supp_graph = {
    'A' : ['B', 'E'],
    'B' : ['A'],
    'E' : ['A'],
}

manuf_graph = {
    'D' : ['G'],
    'G' : ['D'],
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
        print(hospital)
        print(date)
        print(objs)
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
    dates = dict()
    data = []
    objs = supp_inv.objects.filter(sold=True)
    start = time.time()
    
    for obj in objs:
        if obj.itemname not in counts.keys():
            counts[obj.itemname] = obj.quantity
        else:
            counts[obj.itemname]+=obj.quantity
        if obj.itemname not in dates.keys():
            dates[obj.itemname] = obj.date
        else:
            dates[obj.itemname] = min(dates[obj.itemname], obj.date)
    
    for key, value in counts.items():
        temp = (key, dates[key], value)
        data.append(temp)
    # print(data)
    # counts = dict(sorted(counts.items(), key=lambda item: item[1]))

    data.sort(key=lambda i: ( i[1], i[2] ))
    

    end = time.time()-start


    

    print(counts)

    return render(request, 'hospital/metric_04.html', context={"data": data, "supplier": supplier, "exectime": end})



def metric_05_viewpage(request, hospital='B'):
    """ Look at nearby hospitals and find the most prescribed drug. """

    visited = dict()
    max_depth = 2
    counts = dict()
    queue = [hospital]
    visited[hospital] = 0

    while(len(queue)>0):
        t = queue[0]
        queue.pop(0)

        for j in graph[t]:
            if visited[t] < max_depth and j not in visited.keys():
                queue.append(j)
                visited[j] = visited[t]+1
    
    hosp_list = dict()
    start = time.time()

    time_counts = dict()

    for i in range(8):
        date = datetime.date.today() - datetime.timedelta(days=i)
        
        for hosp in visited.keys():
            t1 = time.time()
            objs = hosp_req.objects.filter(hosp_name=hosp, date=date)

            for obj in objs:
                if obj.itemname not in counts.keys():
                    counts[obj.itemname] = obj.quantity
                else:
                    counts[obj.itemname]+=obj.quantity

                if obj.itemname not in hosp_list.keys():
                    hosp_list[obj.itemname] = [hosp]
                elif hosp not in hosp_list[obj.itemname]:
                    hosp_list[obj.itemname].append(hosp)
            
            t2 = time.time()-t1
            # print(t2)
            if hosp not in time_counts.keys():
                time_counts[hosp]=t2
            else:
                time_counts[hosp]+=t2
            


        
    
    end = time.time()-start
    results = dict()
    for i in range(3):
        results[i]=end
    
    for hosp in visited.keys():
        results[visited[hosp]] = min(results[visited[hosp]], time_counts[hosp])
    
    print("TOTAL TIME = ")
    x = 0
    for i in range(3):
        x+=results[i]
    print(x, "seconds")
    print("Expected = ", end)


    counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    data = []

    for key, value in counts.items():
        temp = [key, value, hosp_list[key]]
        data.append(temp)

    print(data)

    return render(request, 'hospital/metric_05.html', context={"data": data, "hospital": hospital, "exectime": end, "paralleltime": x})


def metric_06_viewpage(request, supplier='B'):
    """ Look at nearby suppliers and find the most stocked drug. """

    visited = dict()
    max_depth = 2
    counts = dict()
    queue = [supplier]
    visited[supplier] = 0

    while(len(queue)>0):
        t = queue[0]
        queue.pop(0)

        for j in supp_graph[t]:
            if visited[t] < max_depth and j not in visited.keys():
                queue.append(j)
                visited[j] = visited[t]+1
    
    supp_list = dict()
    start = time.time()
    time_counts = dict()

    for supp in visited.keys():
        t1 = time.time()
        objs = supp_inv.objects.filter(supp_name=supp, sold=False)

        for obj in objs:
            if obj.itemname not in counts.keys():
                counts[obj.itemname] = obj.quantity
            else:
                counts[obj.itemname]+=obj.quantity

            if obj.itemname not in supp_list.keys():
                supp_list[obj.itemname] = [supp]
            elif supp not in supp_list[obj.itemname]:
                supp_list[obj.itemname].append(supp)
        
        t2 = time.time() - t1
        time_counts[supp] = t2

    
    
    end = time.time()-start
    timers = dict()
    for i in range(3):
        timers[i]=end
    
    for supp in visited.keys():
        timers[visited[supp]] = min(timers[visited[supp]], time_counts[supp])

    x = 0;
    for i in range(3):
        x+=timers[i]

    counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    data = []

    for key, value in counts.items():
        temp = [key, value, supp_list[key]]
        data.append(temp)
    
    data.sort(key=lambda i: ( -1*i[1], -1*len(i[2]) ))

    print(data)
    print(x)
    print(end)
    return render(request, 'hospital/metric_06.html', context={"data": data, "supplier": supplier, "exectime": end, "paralleltime": x})



def add_manuf(request):
    
    return redirect("/")


def random_manuf_making():
    new_manuf_making= manuf_making()
    new_manuf_making.man_name = random.choice(manufs)
    print(new_manuf_making.man_name)
    
    new_manuf_making.itemname = random.choice(drugnames)
    quantity  = random.randint(100, 1000)
    
    new_manuf_making.cleared = random.choice([True, False])
    new_manuf_making.quantity = quantity

    new_manuf_making.date_of_production = datetime.date.today() + datetime.timedelta(days=random.randint(-8,8))
    return new_manuf_making

def fill_manuf_making(request):
    counts = 0
    for i in range(n_items):
        new_manuf_making = random_manuf_making()

        try:
            new_manuf_making.save()
            
        except Exception:
            print("Triggered")
            count+=1
            pass
    print("Count ", counts)

    return redirect('/')


def metric_07_viewpage(request, manuf='D'):
    """ Look at nearby manufacturers and find the most produced drug. """

    visited = dict()
    max_depth = 2
    counts = dict()
    queue = [manuf]
    visited[manuf] = 0

    while(len(queue)>0):
        t = queue[0]
        queue.pop(0)

        for j in manuf_graph[t]:
            if visited[t] < max_depth and j not in visited.keys():
                queue.append(j)
                visited[j] = visited[t]+1
    
    manuf_list = dict()
    start = time.time()

    for man in visited.keys():
        objs = manuf_making.objects.filter(man_name=man, cleared=False)

        for obj in objs:
            if obj.itemname not in counts.keys():
                counts[obj.itemname] = obj.quantity
            else:
                counts[obj.itemname]+=obj.quantity

            if obj.itemname not in manuf_list.keys():
                manuf_list[obj.itemname] = [man]
            elif man not in manuf_list[obj.itemname]:
                manuf_list[obj.itemname].append(man)

    
    


    counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    data = []

    for key, value in counts.items():
        temp = [key, value, manuf_list[key]]
        data.append(temp)
    
    data.sort(key=lambda i: ( -1*i[1], -1*len(i[2]) ))
    end = time.time()-start
    print(data)

    return render(request, 'hospital/metric_07.html', context={"data": data, "manuf": manuf, "exectime": end})


def metric_08_viewpage(request, hospital='B'):
    """ Look at nearby hospitals and find the most prescribed drug, that is in least production. """

    visited = dict()
    max_depth = 2
    counts = dict()
    queue = [hospital]
    visited[hospital] = 0

    while(len(queue)>0):
        t = queue[0]
        queue.pop(0)

        for j in graph[t]:
            if visited[t] < max_depth and j not in visited.keys():
                queue.append(j)
                visited[j] = visited[t]+1
    
    hosp_list = dict()
    counts_list = dict()

    time_counts = dict()

    start = time.time()
    
    for i in range(8):
        date = datetime.date.today() - datetime.timedelta(days=i)
        for hosp in visited.keys():
            t1 = time.time()
            objs = hosp_req.objects.filter(hosp_name=hosp, date=date)

            for obj in objs:
                if obj.itemname not in counts.keys():
                    counts[obj.itemname] = obj.quantity
                else:
                    counts[obj.itemname]+=obj.quantity

                if obj.itemname not in hosp_list.keys():
                    hosp_list[obj.itemname] = [hosp]
                elif hosp not in hosp_list[obj.itemname]:
                    hosp_list[obj.itemname].append(hosp)
            
            t2 = time.time()-t1
            if hosp not in time_counts.keys():
                time_counts[hosp]=t2
            else:
                time_counts[hosp]+=t2

    for name in counts.keys():
        counts_list[name]=0
        objs = manuf_making.objects.filter(cleared=False, itemname=name)
        
    
        for obj in objs:
            counts_list[obj.itemname]+=obj.quantity
    
    


    counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    data = []

    for key, value in counts.items():
        temp = [key, value, hosp_list[key], counts_list[key]]
        data.append(temp)

    data.sort(key=lambda i: ( i[3]/i[1] ))

    end = time.time()-start
    results = dict()
    for i in range(3):
        results[i]=end
    
    for hosp in visited.keys():
        results[visited[hosp]] = min(results[visited[hosp]], time_counts[hosp])
    
    print("TOTAL TIME = ")
    x = 0
    for i in range(3):
        x+=results[i]
    print(x, "seconds")
    print("Expected = ", end)
    print(data)

    return render(request, 'hospital/metric_08.html', context={"data": data, "hospital": hospital, "exectime": end, "paralleltime": x})