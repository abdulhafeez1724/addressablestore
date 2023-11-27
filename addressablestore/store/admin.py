from django.contrib import admin
from .models import AppUser, Listing, Transaction

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Listing)
admin.site.register(Transaction)