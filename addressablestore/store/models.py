from django.db import models
from django.utils.crypto import get_random_string

class LoginUser(models.Model):
    unique_id = models.CharField(max_length=6, unique=True, blank=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        return get_random_string(length=6, allowed_chars='0123456789')

    def __str__(self):
        return f"User {self.unique_id} created at {self.created_at}"

class MarketplaceItem(models.Model):
    CATEGORY_CHOICES = [
        ('bus', 'Bus'),
        ('bike', 'Bike'),
        ('character', 'Character'),
    ]

    STATUS_CHOICES = [
        ('for_sale', 'For Sale'),
        ('sold_out', 'Sold Out'),
        ('pending', 'Pending'),
    ]

    data = models.TextField()  
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='for_sale')
    price = models.IntegerField() 

    # Reference to the user who listed the item
    listed_by = models.ForeignKey(LoginUser, on_delete=models.CASCADE, related_name='listed_items')

    def __str__(self):
        return f"Item {self.id} - {self.category} - {self.status} - Price: {self.price} coins"
