from django.contrib import admin
from .models import hosp_inv, hosp_req, supp_storage, supp_inv, manuf_making



# Register your models here.

class HospInvAdmin(admin.ModelAdmin):
    list_display = ('itemname', 'quantity', 'hosp_name')

class HospReqAdmin(admin.ModelAdmin):
    list_display = ('itemname', 'quantity', 'hosp_name', 'date')

class SuppStorAdmin(admin.ModelAdmin):
    list_display = ('supp_name', 'maximum', 'occupied')

def mark_sold(modeladmin, request, queryset):
    
    for obj in queryset:
        if obj.sold == False:
            storage = supp_storage.objects.get(supp_name=obj.supp_name)
            storage.occupied -= obj.quantity
            storage.save()
            obj.sold = True
            obj.save()

mark_sold.short_description = "Mark items as sold"

class SuppInvAdmin(admin.ModelAdmin):
    list_display = ('supp_name', 'itemname', 'date', 'quantity', 'sold')
    actions=[mark_sold]


def mark_cleared(modeladmin, request, queryset):
    
    for obj in queryset:
        if obj.sold == False:
            obj.cleared = True
            obj.save()

mark_cleared.short_description = "Mark stock as cleared"

class ManufMakingAdmin(admin.ModelAdmin):
    list_display=('man_name', 'itemname', 'date_of_production', 'cleared')
    actions=[mark_cleared]



admin.site.register(hosp_inv, HospInvAdmin)
admin.site.register(hosp_req, HospReqAdmin)
admin.site.register(supp_storage, SuppStorAdmin)
admin.site.register(supp_inv, SuppInvAdmin)
admin.site.register(manuf_making, ManufMakingAdmin)
