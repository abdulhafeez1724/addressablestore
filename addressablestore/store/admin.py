from django.contrib import admin
from .models import User, MarketplaceItem

# Register your models here.
admin.site.register(User)
admin.site.register(MarketplaceItem)