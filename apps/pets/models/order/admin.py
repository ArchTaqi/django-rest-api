from django.contrib import admin
from .model import Order

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'pet', 'created_at', 'updated_at',  'complete', ]
    list_display_links = ['id', ]
    list_editable = ['pet', 'complete']
    list_filter = ['complete', 'updated_at', ]
    search_fields = ['pet', ]
    date_hierarchy = 'updated_at'
    ordering = ['pet', ]
