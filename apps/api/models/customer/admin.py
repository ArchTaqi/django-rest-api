from django.contrib import admin
from .model import Customer

# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'updated_at', ]
    list_filter = ['email', ]
    search_fields = ['name']
    list_per_page = 50
