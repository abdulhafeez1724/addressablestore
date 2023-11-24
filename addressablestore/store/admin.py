from django.contrib import admin
from .models import AppUser, Listing

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Listing)