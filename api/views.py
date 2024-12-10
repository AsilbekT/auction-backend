from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from .models import  Email, Lead, Phone, Property, Owner, LegalProceeding, Auction, SalesInformation, Connection, MortgageAndDebt, TaxLien, DuplicateCheck,User
from .serializers import (
    UserSerializer,
    EmailSerializer,
    FullLeadSerializer,
    GetLeadSerializer,
    PhoneSerializer,
    OwnerSerializer,
    LegalProceedingSerializer,
    ReadAuctionSerializer,
    ReadPropertySerializer,
    SalesInformationSerializer,
    ConnectionSerializer,
    MortgageAndDebtSerializer,
    SmallLeadSerializer,
    SmallOwnerSerializer,
    SmallPhoneSerializer,
    TaxLienSerializer,
    DuplicateCheckSerializer,
    WriteAuctionSerializer,
    WriteOwnerSerializer,
    WritePropertySerializer

)
from rest_framework import serializers
from rest_framework.response import Response
from .utils import check_priority, response_success, response_error, CustomPagination, standardize_address



class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadPropertySerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return WritePropertySerializer
        return ReadPropertySerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()



class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'create':
            return SmallOwnerSerializer
        elif self.action == 'create':
            return WriteOwnerSerializer
        return OwnerSerializer


class LegalProceedingViewSet(viewsets.ModelViewSet):
    queryset = LegalProceeding.objects.all().order_by("-id")
    serializer_class = LegalProceedingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadAuctionSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return WriteAuctionSerializer
        return ReadAuctionSerializer

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SalesInformationViewSet(viewsets.ModelViewSet):
    queryset = SalesInformation.objects.all().order_by("-id")
    serializer_class = SalesInformationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all().order_by("-id")
    serializer_class = ConnectionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class MortgageAndDebtViewSet(viewsets.ModelViewSet):
    queryset = MortgageAndDebt.objects.all().order_by("-id")
    serializer_class = MortgageAndDebtSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class TaxLienViewSet(viewsets.ModelViewSet):
    queryset = TaxLien.objects.all().order_by("-id")
    serializer_class = TaxLienSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class DuplicateCheckViewSet(viewsets.ModelViewSet):
    queryset = DuplicateCheck.objects.all().order_by("-id")
    serializer_class = DuplicateCheckSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created, message = self.perform_create(serializer)
        print(created, message)
        if not created:
            return response_error("error", message, http_status=status.HTTP_409_CONFLICT)
        
        return response_success("Success", serializer.data)

    def perform_create(self, serializer):
        standardized_address = standardize_address(serializer.validated_data.get("reformatted_address"))
        source_name = serializer.validated_data.get("source_name")
        is_auction = serializer.validated_data.get("is_auction")
        if any([standardized_address, source_name, is_auction]) == None:
            return False, "All fields must be provided"
        
        if standardized_address is None:
            return False, "Invalid address format"

        existing_duplicate = DuplicateCheck.objects.filter(reformatted_address=standardized_address,is_auction=is_auction)
        if existing_duplicate.exists():
            duplicate_obj = existing_duplicate.last()
            is_important, priority_message = check_priority(
                source_name,
                duplicate_obj
            )
            
            if is_important:
                existing_duplicate.first().delete()
                return True, "Duplicate address updated with new information"
            
            return False, priority_message

        serializer.save(reformatted_address=standardized_address)
        return True, "Duplicate check object created successfully."


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['list']:
            return SmallLeadSerializer
        elif self.action in ['retrieve']:
            return GetLeadSerializer
        return FullLeadSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data

        duplicate_check_data = data.pop("duplicate_check", None)
        owner_data = data.pop("owner", None)
        property_data = data.pop("property", None)
        auction_data = data.pop("auction", None)
        taxlien_data = data.pop("taxlien", None)
        mortgageanddebt_data = data.pop("mortgageanddebt", None)
        legalproceeding_data = data.pop("legalproceeding", None)
        salesInformation_data = data.pop("salesInformation", None)
        connections_data = data.pop("connections", [])
        emails_data = data.pop("emails", [])
        phones_data = data.pop("phones", [])
        current_user = request.user

        def create_related_data(serializer_class, related_data):
            if related_data:
                serializer = serializer_class(data=related_data)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
                return instance.id
            return None

        duplicate_check_id = None
        if duplicate_check_data:
            duplicate_serializer = DuplicateCheckSerializer(data=duplicate_check_data)
            duplicate_serializer.is_valid(raise_exception=True)
            duplicate_view = DuplicateCheckViewSet()
            success, message = duplicate_view.perform_create(duplicate_serializer)
            if not success:
                return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)
            duplicate_check_id = duplicate_serializer.instance.id
        
        owner_id = None
        if owner_data:
            owner_serializer = WriteOwnerSerializer(data=owner_data)
            owner_serializer.is_valid(raise_exception=True)
            owner = owner_serializer.save()
            owner_id = owner.id

            for phone in phones_data:
                phone["owner"] = owner_id
                create_related_data(PhoneSerializer, phone)

            for email in emails_data:
                email["owner"] = owner_id
                create_related_data(EmailSerializer, email)

            for connection in connections_data:
                connection["owner"] = owner_id
                create_related_data(ConnectionSerializer, connection)

        property_id = None
        if property_data:
            property_data["dublicate_address"] = duplicate_check_id
            property_serializer = WritePropertySerializer(data=property_data)
            property_serializer.is_valid(raise_exception=True)
            property = property_serializer.save()
            property_id = property.id

            if legalproceeding_data:
                legalproceeding_data["property"] = property_id
                create_related_data(LegalProceedingSerializer, legalproceeding_data)
            if mortgageanddebt_data:
                mortgageanddebt_data["property"] = property_id
                create_related_data(MortgageAndDebtSerializer, mortgageanddebt_data)
            if taxlien_data:
                taxlien_data["property"] = property_id
                create_related_data(TaxLienSerializer, taxlien_data)

        auction_id = None
        if auction_data :
            auction_id = create_related_data(WriteAuctionSerializer, auction_data)

        salesInformation_id = None    
        if salesInformation_data :
            salesInformation_id = create_related_data(SalesInformationSerializer, salesInformation_data)

        lead_data = {
            **data,
            "owner": owner_id,
            "property": property_id,
            "auction": auction_id,
            "sales_information" : salesInformation_id,
            "created_by" : current_user
        }
        lead_serializer = FullLeadSerializer(data=lead_data)
        lead_serializer.is_valid(raise_exception=True)
        lead_serializer.save()

        return Response(lead_serializer.data, status=status.HTTP_201_CREATED)


    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params
        filters = {}

        for key, value in query_params.items():
            if "__" in key: 
                filters[key] = value

        if filters:
            try:
                queryset = queryset.filter(**filters)
            except Exception as e:
                raise ValidationError(f"Error applying filters: {str(e)}")
            
        sort = self.request.query_params.get('sort', None)
        if sort:
            sort_fields = sort.split(',')
            queryset = queryset.order_by(*sort_fields)

        return queryset

class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return SmallPhoneSerializer
        return PhoneSerializer

class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return EmailSerializer
        return EmailSerializer






