
from django.contrib import admin
from .models import Properties, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'location',
        'price',
        'published',
        'available',
    )
    list_filter = ('published', 'available', 'purpose', 'property_type')
    search_fields = ('title', 'location', 'city')
    inlines = [PropertyImageInline]


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'image_type')
