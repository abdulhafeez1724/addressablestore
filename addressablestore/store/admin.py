from django.contrib import admin
from .models import LoginUser, MarketplaceItem

# Register your models here.
admin.site.register(LoginUser)
admin.site.register(MarketplaceItem)