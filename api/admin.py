from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

class RealEstateAdminSite(AdminSite):
    site_header = 'Real Estate Management Dashboard'
    site_title = 'Real Estate Admin Portal'
    index_title = 'Real Estate Operations'

admin_site = RealEstateAdminSite(name='real_estate_admin')

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

from .models import (
    DuplicateCheck, Property, Owner, LegalProceeding,
    Auction, Connection, Phone, Email,
    MortgageAndDebt, TaxLien, SalesInformation, Lead
)

@admin.register(DuplicateCheck, site=admin_site)
class DuplicateCheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'reformatted_address', 'source_name', 'is_auction', 'created_at', 'updated_at')
    search_fields = ('reformatted_address', 'source_name')
    list_filter = ('is_auction', 'source_name')

@admin.register(Property, site=admin_site)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'city', 'state', 'zip_code', 'property_type', 'zestimate', 'created_at')
    search_fields = ('address', 'city', 'zip_code')
    list_filter = ('city', 'state', 'property_type')

@admin.register(Owner, site=admin_site)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'dob', 'dod', 'mailing_address')
    search_fields = ('first_name', 'last_name', 'mailing_address')
    list_filter = ('mailing_state',)


@admin.register(LegalProceeding, site=admin_site)
class LegalProceedingAdmin(admin.ModelAdmin):
    list_display = ('id', 'case_type', 'property', 'total_amount_owed', 'date_of_filing')
    search_fields = ('case_type', 'property__address')
    list_filter = ('case_type',)

@admin.register(Auction, site=admin_site)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'auction_date', 'estimated_resale_value', 'opening_bid')
    search_fields = ('auction_date',)

@admin.register(Connection, site=admin_site)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'connection_type', 'name')
    search_fields = ('owner__first_name', 'owner__last_name', 'name')

@admin.register(Phone, site=admin_site)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'phone_type')
    search_fields = ('phone_number',)

@admin.register(Email, site=admin_site)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'email_address')
    search_fields = ('email_address',)

@admin.register(MortgageAndDebt, site=admin_site)
class MortgageAndDebtAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'mortgage_amount', 'interest_rate')
    search_fields = ('property__address',)

@admin.register(TaxLien, site=admin_site)
class TaxLienAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'lien_amount', 'lien_date')
    search_fields = ('property__address',)

@admin.register(SalesInformation, site=admin_site)
class SalesInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale_date', 'sold_amount', 'sale_status')
    search_fields = ('sale_date',)

@admin.register(Lead, site=admin_site)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'assigned_to', 'stage', 'deal_strength')
    search_fields = ('property__address', 'assigned_to')
