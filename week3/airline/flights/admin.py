from django.contrib import admin

from .models import Flight, Airport, Passenger

# You can use some settings from django for gui

# Register your models here.
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Passenger)