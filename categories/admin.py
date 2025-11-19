from django.contrib import admin
from .models import Category
from mptt.admin import MPTTModelAdmin

admin.site.register(Category, MPTTModelAdmin)


