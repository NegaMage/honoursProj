from django.contrib import admin
from .models import hosp_est, hosp_inv, hosp_req
# , hosp_emp



# Register your models here.

class HospInvAdmin(admin.ModelAdmin):
    list_display = ('itemname', 'quantity', 'hosp_name')

class HospReqAdmin(admin.ModelAdmin):
    list_display = ('itemname', 'quantity', 'hosp_name', 'date')

admin.site.register(hosp_est)
admin.site.register(hosp_inv, HospInvAdmin)
admin.site.register(hosp_req, HospReqAdmin)
# admin.site.register(hosp_emp)