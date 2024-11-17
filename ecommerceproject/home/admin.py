from django.contrib import admin
from .models import Category, Product, Contact

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'date_submitted', 'is_resolved')
    list_filter = ('department', 'is_resolved', 'date_submitted')
    search_fields = ('name', 'email', 'message')
    ordering = ('-date_submitted',)

