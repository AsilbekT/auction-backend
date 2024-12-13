from django.db import models
from django.contrib.auth.models import User


class DuplicateCheck(models.Model):
    SOURCE_NAME = [
        ("Auction.com", 'auction.com'),
        ("Foreclosure.com", 'foreclosure.com'),
        ("Salesweb", 'salesweb'),
        ("Realtybid", 'realtybid'),
        ("Njcourt", 'njcourt'),
        ("Bids", 'bids'),
        ("FL", 'fl'),
        ("Xome", 'xome'),
        ("ASAP", 'asap'),
    ]

    reformatted_address = models.CharField(max_length=255)
    source_name = models.CharField(max_length=20, choices=SOURCE_NAME)
    is_auction = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.reformatted_address
    
    class Meta:
        db_table = 'duplicate_checks'
        verbose_name = "Duplicate Check"
        verbose_name_plural = "Duplicate Checks"
        indexes = [
            models.Index(fields=['source_name'], name='idx_source_name'),
            models.Index(fields=['reformatted_address'], name='idx_reformatted_address')
        ]

class Property(models.Model):
    dublicate_address = models.ForeignKey(DuplicateCheck, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255, help_text="The full street address of the property")
    city = models.CharField(max_length=100, blank=True, null=True, help_text="The city where the property is located")
    state = models.CharField(max_length=100, blank=True, null=True, help_text="The state where the property is located")
    zip_code = models.CharField(max_length=20, blank=True, null=True, help_text="The postal code for the property")
    county = models.CharField(max_length=100, blank=True, null=True, help_text="The county where the property is located")
    apn = models.CharField(max_length=100, blank=True, null=True, help_text="The assessor's parcel number, unique identifier for the property")
    property_type = models.CharField(max_length=50, blank=True, null=True, help_text="The type of property, e.g., Single Family, Multi Family, Commercial")
    lot_size = models.FloatField(null=True,blank=True,default=0, help_text="The size of the property lot in square feet")
    year_built = models.IntegerField(null=True,blank=True,default=0, help_text="The year in which the property was built")
    zillow_link = models.URLField(blank=True, null=True, help_text="A direct link to the property's Zillow page, if available")
    occupancy_status = models.BooleanField(default=False, blank=True, null=True)
    beds = models.IntegerField(null=True,blank=True,default=0, help_text="Number of bedrooms in the property")
    baths = models.FloatField(null=True,blank=True,default=0, help_text="Number of bathrooms in the property")
    zestimate = models.DecimalField(null=True,blank=True,max_digits=10, decimal_places=2, default=0, help_text="Zillow's estimated market value for the property")
    equity = models.DecimalField(null=True,blank=True,max_digits=12, default=0, decimal_places=2, help_text="Equity amount involved in the property")
    square_footage = models.FloatField(null=True,blank=True,default=0, help_text="Total interior square footage of the property")
    status = models.CharField(max_length=150, blank=True, null=True, help_text="what is the status of property")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    class Meta:
        db_table = 'properties'
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        indexes = [
            models.Index(fields=['city'], name='idx_city'),
            models.Index(fields=['state'], name='idx_state'),
            models.Index(fields=['zip_code'], name='idx_zip_code'),
            models.Index(fields=['county'], name='idx_county'),
            models.Index(fields=['city', 'state'], name='idx_city_state'),
        ]


    def __str__(self):
        return str(self.id)
    

class Owner(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True, help_text="The first name of the property owner")
    last_name = models.CharField(max_length=100, blank=True, null=True,help_text="The last name of the property owner")
    dob = models.DateField(blank=True, null=True , help_text="Date of birth of the property owner")
    dod = models.DateField(blank=True, null=True, help_text="Date of death of the property owner, if applicable")
    mailing_address = models.CharField(blank=True, null=True ,max_length=255, help_text="The mailing address of the property owner")
    mailing_city = models.CharField(blank=True, null=True ,max_length=100, help_text="The city of the mailing address")
    mailing_state = models.CharField(blank=True, null=True ,max_length=100, help_text="The state of the mailing address")
    mailing_zip = models.CharField(blank=True, null=True ,max_length=20, help_text="The ZIP code of the mailing address")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.first_name)
    
    class Meta:
        db_table = 'owners'
        verbose_name = "Owner"
        verbose_name_plural = "Owners"
        indexes = [
            models.Index(fields=['last_name'], name='idx_last_name'),
            models.Index(fields=['mailing_state'], name='idx_mailing_state')
        ]

    
class LegalProceeding(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE,null=True,blank=True, related_name='legal_proceedings',  help_text="The property involved in the legal proceeding")
    document_name = models.CharField(max_length=255, blank=True, null=True , help_text="The name of the legal document")
    case_type = models.CharField(max_length=150, blank=True, null=True, help_text="The type of legal case, e.g., Foreclosure or Lien")
    total_amount_owed = models.DecimalField(max_digits=12, default=0,null=True,blank=True, decimal_places=2, help_text="The total amount owed in the case")
    date_of_filing = models.DateField(blank=True, null=True, help_text="The date on which the legal case was filed")
    plaintiff = models.CharField(blank=True, null=True, max_length=255, help_text="The plaintiff in the legal case")
    plaintiff_attorney_firm = models.CharField(max_length=255, blank=True, null=True, help_text="The law firm representing the plaintiff")
    plaintiff_attorney_name = models.CharField(max_length=255, blank=True, null=True, help_text="The name of the attorney representing the plaintiff")
    plaintiff_atty_bar_no = models.CharField(max_length=100, blank=True, null=True, help_text="Bar number of the plaintiff's attorney")
    defendants = models.TextField(help_text="Text field containing the names of all defendants", blank=True, null=True,)
    probate_case_number = models.CharField(max_length=100, blank=True, null=True, help_text="Case number if the legal proceeding is a probate case")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)
    

    class Meta:
        db_table = 'legal_proceedings'
        verbose_name = "Legal Proceeding"
        verbose_name_plural = "Legal Proceedings"
        indexes = [
            models.Index(fields=['property'], name='idx_property'),
            models.Index(fields=['case_type'], name='idx_case_type')
        ]


class Auction(models.Model):
    auction_date = models.DateField(blank=True, null=True, help_text="The date on which the auction will take place")
    estimated_resale_value = models.DecimalField(max_digits=12,null=True,blank=True, default=0, decimal_places=2, help_text="The estimated resale value of the property at auction")
    opening_bid = models.DecimalField(max_digits=12, default=0,null=True,blank=True, decimal_places=2, help_text="Starting bid for the auction")
    estimated_debt = models.DecimalField(max_digits=12, default=0,null=True,blank=True, decimal_places=2, help_text="Total estimated debt associated with the property")
    rental_estimate = models.DecimalField(max_digits=10, default=0,null=True,blank=True, decimal_places=2, help_text="Estimated rental income the property could generate")
    trustee_sale_number = models.CharField(max_length=100, blank=True, null=True, help_text="A unique identifier assigned to the trustee sale")
    link = models.URLField(blank=True, null=True,help_text="A link to the auction event details")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return str(self.id)


    class Meta:
        db_table = 'auctions'
        verbose_name = "Auction"
        verbose_name_plural = "Auctions"
        indexes = [
            models.Index(fields=['auction_date'], name='idx_auction_date'),
        ]

class Connection(models.Model):
    ASSOCIATE = 'Associate'
    RELATIVE = 'Relative'
    NEIGHBOR = 'Neighbor'
    CONNECTION_TYPES = [
        (ASSOCIATE, 'Associate'),
        (RELATIVE, 'Relative'),
        (NEIGHBOR, 'Neighbor'),
    ]

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE,null=True,blank=True,help_text="The owner associated with this connection")
    connection_type = models.CharField(max_length=10, choices = CONNECTION_TYPES, help_text="The type of connection, e.g., Associate, Relative, Neighbor")
    name = models.CharField(max_length=255, help_text="Full name of the connected individual",null=True,blank=True)
    address = models.CharField(max_length=255, help_text="Address of the connected individual",null=True,blank=True)
    phone = models.CharField(max_length=20, help_text="Phone number of the connected individual",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'owner_connections' 


class Phone(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE,null=True,blank=True, help_text="The phone record belongs to which owner")
    phone_type = models.CharField(max_length=100,null=True,blank=True,help_text="The type of phone, e.g., Mobile, Home, Work")
    phone_connected = models.BooleanField(null=True,blank=True, help_text="Indicator of whether the phone number is active and connected")
    phone_number = models.CharField(max_length=20, help_text="The phone number")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.phone_number

    class Meta:
        db_table = 'owner_phones' 

class Email(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE,null=True,blank=True, help_text="The email record belongs to which owner")
    email_address = models.EmailField(help_text="The email address")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.email_address

    class Meta:
        db_table = 'owner_emails'

class MortgageAndDebt(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE,null=True,blank=True, help_text="The property associated with this mortgage or debt", related_name='mortgages_and_debts')
    mortgage_date = models.DateField(blank=True, null=True, help_text="The date the mortgage was registered")
    mortgage_amount = models.DecimalField(max_digits=12, default=0,null=True,blank=True, decimal_places=2, help_text="The amount of the mortgage")
    interest_rate = models.FloatField(default=0,null=True,blank=True, help_text="The interest rate of the loan")
    loan_type = models.CharField(max_length= 150, blank=True, null=True, help_text="The type of loan, e.g., Primary, Secondary")
    lender_name = models.CharField(max_length=255, blank=True, null=True, help_text="The name of the lender")
    debt = models.DecimalField(max_digits=12, default=0,null=True,blank=True ,decimal_places=2, help_text="The amount of the debt")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'property_mortgages_debts'

class TaxLien(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE,null=True,blank=True, help_text="The property on which the tax lien is placed", related_name='tax_liens')
    lien_type = models.CharField(blank=True, null=True, max_length=150, help_text="The type of tax lien")
    lien_date = models.DateField(blank=True, null=True, help_text="The date the tax lien was placed")
    lien_amount = models.DecimalField(default=0, max_digits=12,null=True,blank=True, decimal_places=2, help_text="The amount of the lien")
    certificate_of_release = models.CharField(max_length=200,blank=True, null=True, help_text="details about the release of the lien, if applicable")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'property_tax_liens'



class SalesInformation(models.Model):
    sale_date = models.DateField(blank=True, null=True, help_text="The date on which the sale is completed or expected to be completed")
    sold_amount = models.DecimalField(max_digits=12, default=0,null=True,blank=True, decimal_places=2, help_text="The amount for which the property was sold")
    sale_status = models.CharField(max_length=100, blank=True, null=True, help_text="The status of the sale, e.g., Pending or Closed")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)
    

    class Meta:
        db_table = 'sales_information' 


class Lead(models.Model):
    sales_information = models.ForeignKey(SalesInformation, on_delete=models.CASCADE, blank=True, null=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(Owner, models.CASCADE, blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True , related_name='assigned_to_users')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_users')
    stage = models.CharField(max_length=50, default="NEW",blank=True, null=True, help_text="The stage of the sales process, e.g., Initial or Follow-Up")
    deal_strength = models.CharField(max_length=100, blank=True, null=True, help_text="An assessment of the deal strength or likelihood to close successfully")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'lead'
