from django.contrib import admin
from .model import Pet, PetCategory, Tag
# Register your models here.


@admin.register(PetCategory)
class PetCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at',  'active', ]
    list_display_links = ['id', ]
    list_editable = ['name', 'active']
    list_filter = ['active', ]
    search_fields = ['name', ]
    date_hierarchy = 'created_at'
    ordering = ['name', ]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at',  'active', ]
    list_display_links = ['id', ]
    list_editable = ['name', 'active']
    list_filter = ['active', ]
    search_fields = ['name', ]
    date_hierarchy = 'created_at'
    ordering = ['name', ]

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at',  'status', ]
    list_display_links = ['id', ]
    list_editable = ['name', 'status']
    list_filter = ['status', 'updated_at', 'category', 'tags', ]
    search_fields = ['name', ]
    date_hierarchy = 'updated_at'
    ordering = ['name', ]