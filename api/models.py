from django.db import models
from django.db.models import JSONField


class Address(models.Model):
    full_address = models.CharField(max_length=255, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=15)
    county = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.full_address

class Property(models.Model):
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=100, blank=True, null=True)
    beds = models.IntegerField(blank=True, null=True)
    baths = models.FloatField(blank=True, null=True)
    square_footage = models.IntegerField(blank=True, null=True)
    lot_size = models.FloatField(blank=True, null=True)  # Consider units here, sqft or acres
    year_built = models.IntegerField(blank=True, null=True)
    owner_occupied = models.BooleanField(default=False)
    additional_details = JSONField(blank=True, null=True)  # To store variable data from other APIs

    def __str__(self):
        return f"{self.address.full_address} - {self.property_type}"

    class Meta:
        ordering = ['id']

class Auction(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    auction_date = models.DateTimeField()
    est_resale_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    opening_bid = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    est_debt = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    rental_estimate = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    link = models.URLField(max_length=1024, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)  # Source of the auction
    event_id = models.CharField(max_length=255, blank=True, null=True)
    trustee_sale_number = models.CharField(max_length=255, blank=True, null=True)
    apn = models.CharField(max_length=255, blank=True, null=True)  # Assessor's Parcel Number

    def __str__(self):
        return f"{self.property.address.full_address} - Auction on {self.auction_date}"

class Ownership(models.Model):
    property = models.ForeignKey(Property, related_name='ownerships', on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=255)
    mailing_address = models.CharField(max_length=255)
    mailing_city = models.CharField(max_length=100)
    mailing_state = models.CharField(max_length=50)
    mailing_zip = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.owner_name} - {self.property.address.full_address}"

class Financial(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    last_sale_date = models.DateField(blank=True, null=True)
    last_sale_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total_assessed_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    assessed_land_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    loans_details = JSONField(blank=True, null=True)  # Dynamic field for multiple loans

    def __str__(self):
        return f"Financials for {self.property.address.full_address}"

