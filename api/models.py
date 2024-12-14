from django.db import models

class Customer(models.Model):
    customer_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=1)
    device_type = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100)
    home_location_lat = models.FloatField()
    home_location_long = models.FloatField()
    home_country = models.CharField(max_length=100)
    first_join_date = models.DateTimeField()

class Product(models.Model):
    product_id = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10)
    masterCategory = models.CharField(max_length=100)
    subCategory = models.CharField(max_length=100)
    articleType = models.CharField(max_length=100)
    baseColour = models.CharField(max_length=50)
    season = models.CharField(max_length=50)
    year = models.IntegerField()
    usage = models.CharField(max_length=100)
    productDisplayName = models.CharField(max_length=200)

class Transaction(models.Model):
    created_at = models.DateTimeField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=100, unique=True)
    session_id = models.CharField(max_length=100)
    product_metadata = models.JSONField()
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=10)
    promo_amount = models.FloatField()
    promo_code = models.CharField(max_length=100, null=True, blank=True)
    shipment_fee = models.FloatField()
    shipment_date_limit = models.DateTimeField()
    total_amount = models.FloatField()
