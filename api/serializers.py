from rest_framework import serializers
from .models import Property, Owner, Ownership, LegalProceeding, Auction, SalesInformation, Connection, ContactInformation, Phone, Email, MortgageAndDebt, TaxLien, DuplicateCheck


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'


class ContactInformationSerializer(serializers.ModelSerializer):
    phones = PhoneSerializer(many=True, read_only=True, source='phone_set')
    emails = EmailSerializer(many=True, read_only=True, source='email_set')

    class Meta:
        model = ContactInformation
        fields = '__all__'


class OwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ownership
        fields = '__all__'


class OwnerSerializer(serializers.ModelSerializer):
    ownerships = OwnershipSerializer(many=True, read_only=True, source='ownership_set')
    contact_information = ContactInformationSerializer(many=True, read_only=True, source='contactinformation_set')

    class Meta:
        model = Owner
        fields = '__all__'


class LegalProceedingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalProceeding
        fields = '__all__'

class SalesInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInformation
        fields = '__all__'



class AuctionSerializer(serializers.ModelSerializer):
    sales_information = SalesInformationSerializer(many=True, read_only=True, source='salesinformation_set')

    class Meta:
        model = Auction
        fields = [
            'id', 'auction_date', 'estimated_resale_value', 'opening_bid', 'estimated_debt', 
            'rental_estimate', 'event_id', 'trustee_sale_number', 'link', 'property', 'sales_information'
        ]


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'


class MortgageAndDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortgageAndDebt
        fields = '__all__'


class TaxLienSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxLien
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'address', 'city', 'state', 'zip_code', 'beds', 'baths']  # Basic fields


class SmallPropertySerializer(PropertySerializer):
    class Meta:
        model = Property
        fields = ['id', 'address', 'city', 'state', 'zip_code', 'beds', 'baths']


class FullPropertySerializer(serializers.ModelSerializer):
    ownerships = OwnershipSerializer(many=True, read_only=True) 
    legal_proceedings = LegalProceedingSerializer(many=True, read_only=True)
    auctions = AuctionSerializer(many=True, read_only=True) 
    mortgages_and_debts = MortgageAndDebtSerializer(many=True, read_only=True)  
    tax_liens = TaxLienSerializer(many=True, read_only=True) 

    class Meta:
        model = Property
        fields = [
            'id', 'address', 'city', 'state', 'zip_code', 'county', 'apn', 'property_type',
            'lot_size', 'year_built', 'zillow_link', 'occupancy_status', 'beds', 'baths',
            'zestimate', 'square_footage', 'ownerships', 'legal_proceedings', 'auctions',
            'mortgages_and_debts', 'tax_liens'
        ]



class DuplicateCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = DuplicateCheck
        fields = '__all__'
