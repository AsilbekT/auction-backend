from django.contrib import admin
from .models import Address, Property, Auction, Ownership, Financial

class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_address', 'city', 'state', 'zip_code', 'county')
    search_fields = ('full_address', 'city', 'state', 'zip_code')

admin.site.register(Address, AddressAdmin)

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('address', 'property_type', 'beds', 'baths', 'square_footage', 'year_built')
    list_filter = ('property_type', 'beds', 'baths', 'year_built')
    search_fields = ('address__full_address', 'property_type')

admin.site.register(Property, PropertyAdmin)

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('property', 'auction_date', 'est_resale_value', 'opening_bid', 'source')
    list_filter = ('auction_date', 'source')
    search_fields = ('property__address__full_address', 'event_id', 'trustee_sale_number')

admin.site.register(Auction, AuctionAdmin)

class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('owner_name', 'property', 'mailing_address')
    search_fields = ('owner_name', 'property__address__full_address')
    list_filter = ('mailing_state',)

admin.site.register(Ownership, OwnershipAdmin)

class FinancialAdmin(admin.ModelAdmin):
    list_display = ('property', 'last_sale_date', 'last_sale_price', 'total_assessed_value')
    list_filter = ('last_sale_date',)
    search_fields = ('property__address__full_address',)

admin.site.register(Financial, FinancialAdmin)
