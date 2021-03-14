from django.contrib import admin
from .models import hosp_est, hosp_inv, hosp_req, hosp_emp



# Register your models here.

admin.site.register(hosp_est)
admin.site.register(hosp_inv)
admin.site.register(hosp_req)
admin.site.register(hosp_emp)