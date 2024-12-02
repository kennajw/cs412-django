# rpg/admin.py
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Character)
admin.site.register(Item)
admin.site.register(Inventory)
admin.site.register(Achievement)