from django.shortcuts import render
from django.http import HttpResponse
from hospital.models import hosp_emp

# def logout_request(request):
#     logout(request)
#     messages.info(request, "Logged out successfully!")
#     return redirect("main:homepage")

def homepage(request):
    # return HttpResponse("<h1> HELLO </h1>")
    # return render(request, 'hospital/home.html')
    return render(request, 'hospital/home.html', context={"objs": hosp_emp.objects.all})