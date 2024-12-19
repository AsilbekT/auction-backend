from rest_framework import serializers
from .models import Lead, Property, Owner, LegalProceeding, Auction, SalesInformation, Connection, Phone, Email, MortgageAndDebt, TaxLien, DuplicateCheck, User
from django.utils import timezone

class BaseUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        # Fetch the data passed in the request
        request_data = self.context['request'].data

        # Update all fields on the instance using the raw request data
        for field, value in request_data.items():
            if hasattr(instance, field):  # Ensure the field exists in the model
                setattr(instance, field, value)

        # Save the updated instance
        instance.save()
        return instance
    
#user serializers
class CreateOrReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UpdateOrDeleteUserSerializer(BaseUpdateSerializer):
    class Meta:
        model = User
        fields = ['id']

class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name']
        
#phone serializers
class CreateOrReadPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'

class UpdateOrDeletePhoneSerializer(BaseUpdateSerializer):
    class Meta:
        model = Phone
        fields = ['id']

class ListPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ['id','phone_number']

 #email serializers      
class CreateOrReadEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'

class UpdateOrDeleteEmailSerializer(BaseUpdateSerializer):
    class Meta:
        model = Email
        fields = ['id']

class ListEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['id','email_address']


#legalprocceding serializers
class CreateOrReadLegalProceedingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalProceeding
        fields = '__all__'

class UpdateOrDeleteLegalProceedingSerializer(BaseUpdateSerializer):
    class Meta:
        model = LegalProceeding
        fields = ['id']

class ListLegalProceedingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalProceeding
        fields = ['id','document_name']

#salesinformation serializers
class CreateOrReadSalesInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInformation
        fields = '__all__'

class UpdateOrDeleteSalesInformationSerializer(BaseUpdateSerializer):
    class Meta:
        model = SalesInformation
        fields = ['id'] 

class ListSalesInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInformation
        fields = ['id','sale_date']

#auction serializers
class CreateOrReadAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'

class UpdateOrDeleteAuctionSerializer(BaseUpdateSerializer):
    class Meta:
        model = Auction
        fields = ['id'] 
        
class ListAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id','auction_date']

#connection serializers
class CreateOrReadConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'

class UpdateOrDeleteConnectionSerializer(BaseUpdateSerializer):
    class Meta:
        model = Connection
        fields = ['id'] 

class ListConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['id','address']

#mortgageanddebt serializers
class CreateOrReadMortgageAndDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortgageAndDebt
        fields = '__all__'

class UpdateOrDeleteMortgageAndDebtSerializer(BaseUpdateSerializer):
    class Meta:
        model = MortgageAndDebt
        fields = ['id']

class ListMortgageAndDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortgageAndDebt
        fields = ['id','debt']
#taxlien serializers
class CreateOrReadTaxLienSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxLien
        fields = '__all__'

class UpdateOrDeleteTaxLienSerializer(BaseUpdateSerializer):
    class Meta:
        model = TaxLien
        fields = ['id']

class ListTaxLienSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxLien
        fields = ['id','lien_amount']

#duplicatecheck serializers
class CreateOrReadDuplicateCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = DuplicateCheck
        fields = '__all__'

class UpdateOrDeleteDuplicateCheckSerializer(BaseUpdateSerializer):
    class Meta:
        model = DuplicateCheck
        fields = ['id']

class ListDuplicateCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = DuplicateCheck
        fields = ['id','reformatted_address']

#property serializers
class ReadPropertySerializer(serializers.ModelSerializer):
    tax_liens = CreateOrReadTaxLienSerializer(many=True, read_only=True,source='tax_lien_set')
    mortgages_and_debts = CreateOrReadMortgageAndDebtSerializer(many=True, read_only=True,source='mortgages_and_debts_set')
    legal_proceedings = CreateOrReadLegalProceedingSerializer(many=True, read_only=True,source='legal_proceeding_set')
    duplicate_check = CreateOrReadDuplicateCheckSerializer(read_only=True,source='properties_set')
    equity = serializers.SerializerMethodField()

    def get_equity(self, obj):
        related_debt = obj.mortgages_and_debts_set.first() 
        debt = related_debt.debt if related_debt else 0 
        return obj.zestimate - debt
    
    class Meta:
        model = Property
        fields = '__all__'

class CreatePropertySerializer(serializers.ModelSerializer):
    duplicate_check = CreateOrReadDuplicateCheckSerializer(read_only=True)
    class Meta:
        model = Property
        fields = '__all__'

class UpdateOrDeletePropertySerializer(BaseUpdateSerializer):
    class Meta:
        model = Property
        fields = ['id']

class ListPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id','address']

class CreateLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

class UpdateOrDeleteLeadSerializer(BaseUpdateSerializer):
    class Meta:
        model = Lead
        fields = ['id']     

class ListLeadSerializer(serializers.ModelSerializer):
    property = ReadPropertySerializer(read_only=True)
    class Meta:
        model = Lead
        fields =  ['id', 'property','assigned_to', 'stage', 'deal_strength','created_by','created_at','updated_at']

#owner
class CreateOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

class ReadOwnerSerializer(serializers.ModelSerializer):
    phones = CreateOrReadPhoneSerializer(many=True, read_only=True,source="phone_set")
    emails = CreateOrReadEmailSerializer(many=True, read_only=True,source="email_set")
    connection = CreateOrReadConnectionSerializer(many=True, read_only=True, source='connection_set')
    class Meta:
        model = Owner
        fields = '__all__'

class UpdateOrDeleteOwnerSerializer(BaseUpdateSerializer):
    class Meta:
        model = Owner
        fields = ['id']

class ListOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id','first_name','last_name']

#lead serializers
class ReadLeadSerializer(serializers.ModelSerializer):
    sales_information = CreateOrReadSalesInformationSerializer(many=True, read_only=True,source='sales_information_set')
    auction = CreateOrReadAuctionSerializer(many=True, read_only=True,source='auction_set')
    property = ReadPropertySerializer(read_only=True)
    owner = ReadOwnerSerializer(many=True, read_only=True,source='owner_set')
    created_by = ListUserSerializer(read_only=True)
    class Meta:
        model = Lead
        fields = '__all__'

    def validate(self, data):
        if self.instance and not any(data.get(field) for field in data):
            raise serializers.ValidationError("At least one field must be provided for update.")
        return data

    def create(self, validated_data):
        return Lead.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.updated_at = timezone.now()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


