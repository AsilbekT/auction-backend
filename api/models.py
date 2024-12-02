from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    SINGLE_FAMILY = 'SF'
    MULTI_FAMILY = 'MF'
    COMMERCIAL = 'CM'
    PROPERTY_TYPES = [
        (SINGLE_FAMILY, 'Single Family'),
        (MULTI_FAMILY, 'Multi Family'),
        (COMMERCIAL, 'Commercial'),
    ]

    VACANT = 'V'
    OCCUPIED = 'O'
    OCCUPANCY_STATUS = [
        (VACANT, 'Vacant'),
        (OCCUPIED, 'Occupied'),
    ]

    address = models.CharField(max_length=255, help_text="The full street address of the property")
    city = models.CharField(max_length=100, help_text="The city where the property is located")
    state = models.CharField(max_length=100, help_text="The state where the property is located")
    zip_code = models.CharField(max_length=20, help_text="The postal code for the property")
    county = models.CharField(max_length=100, help_text="The county where the property is located")
    apn = models.CharField(max_length=100, unique=True, db_index=True, help_text="The assessor's parcel number, unique identifier for the property")
    property_type = models.CharField(max_length=2, choices=PROPERTY_TYPES, help_text="The type of property, e.g., Single Family, Multi Family, Commercial")
    lot_size = models.IntegerField(help_text="The size of the property lot in square feet")
    year_built = models.IntegerField(help_text="The year in which the property was built")
    zillow_link = models.URLField(blank=True, null=True, help_text="A direct link to the property's Zillow page, if available")
    occupancy_status = models.CharField(max_length=1, choices=OCCUPANCY_STATUS, help_text="Occupancy status of the property, e.g., Vacant, Occupied")
    beds = models.IntegerField(help_text="Number of bedrooms in the property")
    baths = models.IntegerField(help_text="Number of bathrooms in the property")
    zestimate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Zillow's estimated market value for the property")
    square_footage = models.IntegerField(help_text="Total interior square footage of the property")

    class Meta:
        indexes = [
            models.Index(fields=['city'], name='city_idx'),
            models.Index(fields=['state'], name='state_idx'),
            models.Index(fields=['city', 'state'], name='city_state_idx'),
        ]

    def __str__(self):
        return str(self.id)
    

class Owner(models.Model):
    property = models.ManyToManyField(Property, through='Ownership')
    first_name = models.CharField(max_length=100, help_text="The first name of the property owner")
    last_name = models.CharField(max_length=100, help_text="The last name of the property owner")
    dob = models.DateField(help_text="Date of birth of the property owner")
    dod = models.DateField(blank=True, null=True, help_text="Date of death of the property owner, if applicable")
    mailing_address = models.CharField(max_length=255, help_text="The mailing address of the property owner")
    mailing_city = models.CharField(max_length=100, help_text="The city of the mailing address")
    mailing_state = models.CharField(max_length=100, help_text="The state of the mailing address")
    mailing_zip = models.CharField(max_length=20, help_text="The ZIP code of the mailing address")

    def __str__(self):
        return str(self.first_name)
    

class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='ownerships')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='ownerships')
    percentage_owned = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Optional
    date_acquired = models.DateField()

class LegalProceeding(models.Model):
    FORECLOSURE = 'FC'
    LIEN = 'LN'
    CASE_TYPES = [
        (FORECLOSURE, 'Foreclosure'),
        (LIEN, 'Lien'),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='legal_proceedings',  help_text="The property involved in the legal proceeding")
    document_name = models.CharField(max_length=255, help_text="The name of the legal document")
    case_type = models.CharField(max_length=2, choices=CASE_TYPES, help_text="The type of legal case, e.g., Foreclosure or Lien")
    total_amount_owed = models.DecimalField(max_digits=12, decimal_places=2, help_text="The total amount owed in the case")
    equity = models.DecimalField(max_digits=12, decimal_places=2, help_text="Equity amount involved in the legal proceeding")
    date_of_filing = models.DateField(help_text="The date on which the legal case was filed")
    plaintiff = models.CharField(max_length=255, help_text="The plaintiff in the legal case")
    plaintiff_attorney_firm = models.CharField(max_length=255, help_text="The law firm representing the plaintiff")
    plaintiff_attorney_name = models.CharField(max_length=255, help_text="The name of the attorney representing the plaintiff")
    plaintiff_atty_bar_no = models.CharField(max_length=100, help_text="Bar number of the plaintiff's attorney")
    defendants = models.TextField(help_text="Text field containing the names of all defendants")
    probate_case_number = models.CharField(max_length=100, help_text="Case number if the legal proceeding is a probate case")

    def __str__(self):
        return str(self.id)
    

class Auction(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='auctions', help_text="Reference to the property being auctioned")
    auction_date = models.DateField(help_text="The date on which the auction will take place")
    estimated_resale_value = models.DecimalField(max_digits=12, decimal_places=2, help_text="The estimated resale value of the property at auction")
    opening_bid = models.DecimalField(max_digits=12, decimal_places=2, help_text="Starting bid for the auction")
    estimated_debt = models.DecimalField(max_digits=12, decimal_places=2, help_text="Total estimated debt associated with the property")
    rental_estimate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Estimated rental income the property could generate")
    event_id = models.CharField(max_length=100, help_text="An identifier for the auction event")
    trustee_sale_number = models.CharField(max_length=100, help_text="A unique identifier assigned to the trustee sale")
    link = models.URLField(help_text="A link to the auction event details")

    def __str__(self):
        return str(self.id)
    
class SalesInformation(models.Model):
    PENDING = 'PD'
    CLOSED = 'CL'
    SALE_STATUSES = [
        (PENDING, 'Pending'),
        (CLOSED, 'Closed'),
    ]

    INITIAL = 'IN'
    FOLLOW_UP = 'FU'
    STAGES = [
        (INITIAL, 'Initial'),
        (FOLLOW_UP, 'Follow-Up'),
    ]

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True, null=True)
    sale_date = models.DateField(help_text="The date on which the sale is completed or expected to be completed")
    sold_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="The amount for which the property was sold")
    sale_status = models.CharField(max_length=2, choices=SALE_STATUSES, help_text="The status of the sale, e.g., Pending or Closed")
    stage = models.CharField(max_length=2, choices=STAGES, help_text="The stage of the sales process, e.g., Initial or Follow-Up")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="The user assigned to manage the sale")
    deal_strength = models.CharField(max_length=100, help_text="An assessment of the deal strength or likelihood to close successfully")

    def __str__(self):
        return str(self.id)
    

class Connection(models.Model):
    ASSOCIATE = 'Associate'
    RELATIVE = 'Relative'
    NEIGHBOR = 'Neighbor'
    CONNECTION_TYPES = [
        (ASSOCIATE, 'Associate'),
        (RELATIVE, 'Relative'),
        (NEIGHBOR, 'Neighbor'),
    ]

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, help_text="The owner associated with this connection")
    connection_type = models.CharField(max_length=10, choices=CONNECTION_TYPES, help_text="The type of connection, e.g., Associate, Relative, Neighbor")
    name = models.CharField(max_length=255, help_text="Full name of the connected individual")
    address = models.CharField(max_length=255, help_text="Address of the connected individual")
    phone = models.CharField(max_length=20, help_text="Phone number of the connected individual")

    def __str__(self):
        return self.name
    
class ContactInformation(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, help_text="The owner for whom this contact information applies")
    
    def __str__(self):
        return self.owner.first_name
    
class Phone(models.Model):
    contact_information = models.ForeignKey(ContactInformation, on_delete=models.CASCADE, help_text="The contact information record to which this phone number belongs")
    phone_type = models.CharField(max_length=100, help_text="The type of phone, e.g., Mobile, Home, Work")
    phone_connected = models.BooleanField(default=False, help_text="Indicator of whether the phone number is active and connected")
    phone_number = models.CharField(max_length=20, help_text="The phone number")

    def __str__(self):
        return self.phone_number
    
class Email(models.Model):
    contact_information = models.ForeignKey(ContactInformation, on_delete=models.CASCADE, help_text="The contact information record to which this email address belongs")
    email_address = models.EmailField(help_text="The email address")
    
    def __str__(self):
        return self.email_address
    
class MortgageAndDebt(models.Model):
    PRIMARY = 'PR'
    SECONDARY = 'SC'
    LOAN_TYPES = [
        (PRIMARY, 'Primary'),
        (SECONDARY, 'Secondary'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, help_text="The property associated with this mortgage or debt", related_name='mortgages_and_debts')
    mortgage_date = models.DateField(help_text="The date the mortgage was registered")
    mortgage_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="The amount of the mortgage")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="The interest rate of the mortgage")
    loan_type = models.CharField(max_length=2, choices=LOAN_TYPES, help_text="The type of loan, e.g., Primary, Secondary")
    lender_name = models.CharField(max_length=255, help_text="The name of the lender")

    def __str__(self):
        return str(self.id)
    
class TaxLien(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, help_text="The property on which the tax lien is placed", related_name='tax_liens')
    lien_type = models.CharField(max_length=100, help_text="The type of tax lien")
    lien_date = models.DateField(help_text="The date the tax lien was placed")
    lien_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="The amount of the lien")
    certificate_of_release = models.JSONField(help_text="JSON field containing details about the release of the lien, if applicable")


    def __str__(self):
        return str(self.id)