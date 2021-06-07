from django.contrib import admin

# Register your models here.

from .models import UserData, Food

admin.site.register(UserData)
admin.site.register(Food)