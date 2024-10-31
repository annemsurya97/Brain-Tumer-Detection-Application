from django.contrib import admin

# Register your models here.
from .models import Test_data

@admin.register(Test_data)
class Admin(admin.ModelAdmin):
    list_display = ['id']
