from django.contrib import admin
from .models import (Property, Auction, SalesInformation, LegalProceeding, Owner,
                     Connection, ContactInformation, Phone, Email, MortgageAndDebt, TaxLien)

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['address', 'city', 'state', 'zip_code', 'property_type', 'occupancy_status']
    search_fields = ['address', 'city', 'apn']
    list_filter = ['city', 'state', 'property_type', 'occupancy_status']

class AuctionAdmin(admin.ModelAdmin):
    list_display = ['property', 'auction_date', 'estimated_resale_value', 'opening_bid']
    list_filter = ['auction_date']
    search_fields = ['property__address']

class SalesInformationAdmin(admin.ModelAdmin):
    list_display = ['auction', 'sale_date', 'sold_amount', 'sale_status', 'stage']
    list_filter = ['sale_status', 'stage']
    search_fields = ['property__address']

class LegalProceedingAdmin(admin.ModelAdmin):
    list_display = ['property', 'document_name', 'case_type', 'date_of_filing']
    list_filter = ['case_type', 'date_of_filing']
    search_fields = ['property__address', 'plaintiff']

from django.contrib import admin
from .models import Owner, Ownership, Property

class OwnershipInline(admin.TabularInline):
    model = Ownership
    extra = 1  # Number of empty forms to display in the inline section
    fields = ('property', 'percentage_owned', 'date_acquired')  # Fields to display in the inline
    autocomplete_fields = ('property',)  # Enables search for related properties


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['owner', 'connection_type', 'name']
    list_filter = ['connection_type']
    search_fields = ['owner__first_name', 'owner__last_name', 'name']

class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ['owner']

class PhoneAdmin(admin.ModelAdmin):
    list_display = ['contact_information', 'phone_type', 'phone_connected', 'phone_number']
    list_filter = ['phone_type', 'phone_connected']
    search_fields = ['phone_number']

class EmailAdmin(admin.ModelAdmin):
    list_display = ['contact_information', 'email_address']
    search_fields = ['email_address']

class MortgageAndDebtAdmin(admin.ModelAdmin):
    list_display = ['property', 'mortgage_date', 'mortgage_amount', 'loan_type']
    list_filter = ['mortgage_date', 'loan_type']
    search_fields = ['property__address']

class TaxLienAdmin(admin.ModelAdmin):
    list_display = ['property', 'lien_type', 'lien_date', 'lien_amount']
    list_filter = ['lien_type', 'lien_date']
    search_fields = ['property__address']

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'dob', 'dod', 'mailing_address', 'mailing_city', 'mailing_state', 'mailing_zip')  # Fields displayed in the admin list view
    search_fields = ('first_name', 'last_name', 'mailing_address')  # Fields available for search
    list_filter = ('mailing_city', 'mailing_state')  # Filters in the right sidebar
    inlines = [OwnershipInline]  # Adds Ownership as an inline to Owner

@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('owner', 'property', 'percentage_owned', 'date_acquired')  # Fields displayed in the admin list view
    search_fields = ('owner__first_name', 'owner__last_name', 'property__address')  # Fields available for search
    list_filter = ('date_acquired',)  # Filters in the right sidebar
    autocomplete_fields = ('owner', 'property')  # Enables search for related owners and properties


admin.site.register(Property, PropertyAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(SalesInformation, SalesInformationAdmin)
admin.site.register(LegalProceeding, LegalProceedingAdmin)
# admin.site.register(Owner, OwnerAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(ContactInformation, ContactInformationAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(MortgageAndDebt, MortgageAndDebtAdmin)
admin.site.register(TaxLien, TaxLienAdmin)
