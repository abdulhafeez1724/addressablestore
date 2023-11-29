from django.db import models

class AppUser(models.Model):
    username = models.CharField(max_length=6, unique=True)
    app_package_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    class Category(models.TextChoices):
        CAR = 'car', 'Car'
        BUS = 'bus', 'Bus'
        BIKE = 'bike', 'Bike'
        CHARACTER = 'character', 'Character'
        PARTS = 'parts', 'Parts'

    class Status(models.TextChoices):
        FOR_SALE = 'for_sale', 'For Sale'
        SOLD_OUT = 'sold_out', 'Sold Out'
        PENDING = 'pending', 'Pending'
        
    class Meta:
        ordering = ['-created_at']

    data = models.TextField()  
    category = models.CharField(max_length=20, choices=Category.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.FOR_SALE)
    price = models.IntegerField()
    listed_by = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    claim = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listed_by} - {self.category} - {self.status} - Price: {self.price} coins"


class Transaction(models.Model):
    buyer = models.ForeignKey(AppUser, related_name='buyer', on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Seller: {self.seller.username}, Buyer: {self.buyer.username}, Listing: {self.listing.id}, Date: {self.transaction_date}"