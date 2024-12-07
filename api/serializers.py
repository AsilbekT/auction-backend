from rest_framework import serializers
from .models import Lead, Property, Owner, Ownership, LegalProceeding, Auction, SalesInformation, Connection, ContactInformation, Phone, Email, MortgageAndDebt, TaxLien, DuplicateCheck
from django.utils import timezone

class SmallPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ['id', 'phone_number', 'phone_type']

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


class BasicContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = '__all__'


class SmallOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ownership
        fields = ['id', 'owner', 'percentage_owned']


class OwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ownership
        fields = '__all__'


class WriteOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

class SmallOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'first_name', 'last_name', 'mailing_address']


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



class ReadAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'auction_date', 'estimated_resale_value', 'opening_bid']


class WriteAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'


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


class DuplicateCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = DuplicateCheck
        fields = ['id', 'reformatted_address', 'source_name', 'is_auction']

class ReadPropertySerializer(serializers.ModelSerializer):
    dublicate_address = DuplicateCheckSerializer(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'address', 'city', 'state', 'zip_code', 'beds', 'baths',
            'dublicate_address', 'created_at', 'updated_at'
        ]


class WritePropertySerializer(serializers.ModelSerializer):
    dublicate_address = serializers.PrimaryKeyRelatedField(
        queryset=DuplicateCheck.objects.all(),
        required=False,
        allow_null=True,
        help_text="ID of the related DuplicateCheck"
    )

    class Meta:
        model = Property
        fields = [
            'id', 'address', 'city', 'state', 'zip_code', 'beds', 'baths',
            'dublicate_address', 'lot_size', 'year_built', 'property_type'
        ]

    def validate(self, data):
        if data.get('dublicate_address') and not DuplicateCheck.objects.filter(id=data['dublicate_address'].id).exists():
            raise serializers.ValidationError("Invalid DuplicateCheck ID.")
        return data

class FullPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'



class DuplicateCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = DuplicateCheck
        fields = '__all__'


class SmallLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'assigned_to', 'stage', 'deal_strength']

class FullLeadSerializer(serializers.ModelSerializer):
    sales_information = serializers.PrimaryKeyRelatedField(queryset=SalesInformation.objects.all(), required=False, allow_null=True)
    auction = serializers.PrimaryKeyRelatedField(queryset=Auction.objects.all(), required=False, allow_null=True)
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), required=False, allow_null=True)
    ownership = serializers.PrimaryKeyRelatedField(queryset=Ownership.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Lead
        fields = [
            'id', 'assigned_to', 'stage', 'deal_strength', 'sales_information', 
            'auction', 'property', 'ownership', 'created_at', 'updated_at'
        ]

    def validate(self, data):
        # During updates, check if at least one field is provided
        if self.instance and not any(data.get(field) for field in data):
            raise serializers.ValidationError("At least one field must be provided for update.")
        return data

    def create(self, validated_data):
        return Lead.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print("updating")
        instance.updated_at = timezone.now()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance





class NestedTaxLienSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxLien
        fields = '__all__'


class NestedMortgageAndDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortgageAndDebt
        fields = '__all__'


class NestedPropertySerializer(serializers.ModelSerializer):
    tax_liens = NestedTaxLienSerializer(many=True, read_only=True)
    mortgages_and_debts = NestedMortgageAndDebtSerializer(many=True, read_only=True)
    legal_proceedings = LegalProceedingSerializer(many=True, read_only=True)
    dublicate_address = DuplicateCheckSerializer(read_only=True)

    class Meta:
        model = Property
        fields = '__all__'


class NestedOwnerSerializer(serializers.ModelSerializer):
    contact_information = ContactInformationSerializer(many=True, read_only=True)
    ownerships = SmallOwnershipSerializer(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = '__all__'

class NestedContactInformationSerializer(serializers.ModelSerializer):
    phones = PhoneSerializer(many=True, read_only=True)
    emails = EmailSerializer(many=True, read_only=True)

    class Meta:
        model = ContactInformation
        fields = '__all__'


class ExpandedOwnershipSerializer(serializers.ModelSerializer):
    ownerships = SmallOwnershipSerializer(many=True, read_only=True)
    contact_information = NestedContactInformationSerializer(many=True, read_only=True)
    connections = ConnectionSerializer(many=True, read_only=True)

    class Meta:
        model = Ownership
        fields = '__all__'



class GetLeadSerializer(serializers.ModelSerializer):
    sales_information = SalesInformationSerializer(read_only=True)
    auction = ReadAuctionSerializer(read_only=True)
    property = NestedPropertySerializer(read_only=True)
    ownership = ExpandedOwnershipSerializer(read_only=True)
    owner = NestedOwnerSerializer(read_only=True, many=True)

    class Meta:
        model = Lead
        fields = [
            'id', 'assigned_to', 'stage', 'deal_strength', 'sales_information', 
            'auction', 'property', 'ownership','owner', 'created_at', 'updated_at'
        ]
