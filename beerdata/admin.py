from django.contrib import admin

from .models import Beer, Brewery
# Register your models here.

admin.site.register(Beer)
admin.site.register(Brewery)
