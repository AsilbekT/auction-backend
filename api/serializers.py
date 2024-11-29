from rest_framework import serializers
from .models import Property, Address

class AddressSerializer(serializers.ModelSerializer):
    full_address = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    unit = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    city = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    state = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    zip_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    county = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Address
        fields = ['full_address', 'unit', 'city', 'state', 'zip_code', 'county']


class PropertySerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)  # Address is now optional

    class Meta:
        model = Property
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        address = Address.objects.create(**address_data) if address_data else None
        property = Property.objects.create(address=address, **validated_data)
        return property

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        address = instance.address

        # Update property fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create address
        if address_data:
            if address:
                for attr, value in address_data.items():
                    setattr(address, attr, value)
                address.save()
            else:
                address = Address.objects.create(**address_data)
                instance.address = address
                instance.save()

        return instance
