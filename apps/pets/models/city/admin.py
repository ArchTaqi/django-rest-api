from django.contrib import admin
from .model import City

# Register your models here.


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', ]
    list_display_links = ['id', ]
    list_editable = ['name',]
    list_filter = ['name', ]
    search_fields = ['name', ]
    date_hierarchy = 'created_at'
    ordering = ['name', ]
