from django.db import models
from django.utils.crypto import get_random_string

class AppUser(models.Model):
    user_id = models.CharField(max_length=10)
    package_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if not self.unique_id:
    #         self.unique_id = self.generate_unique_id()
    #     super().save(*args, **kwargs)

    # def generate_unique_id(self):
    #     return get_random_string(length=6, allowed_chars='0123456789')

    def __str__(self):
        return f"User {self.user_id} created at {self.created_at}"

class Listing(models.Model):
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
    listed_by = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    claim = models.BooleanField(default=False)
    def __str__(self):
        return f"Item {self.id} - {self.category} - {self.status} - Price: {self.price} coins"
