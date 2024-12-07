from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from .models import ContactInformation, Email, Lead, Ownership, Phone, Property, Owner, LegalProceeding, Auction, SalesInformation, Connection, MortgageAndDebt, TaxLien, DuplicateCheck
from .serializers import (
    ContactInformationSerializer,
    EmailSerializer,
    FullLeadSerializer,
    GetLeadSerializer,
    OwnershipSerializer,
    PhoneSerializer,
    PropertySerializer,
    OwnerSerializer,
    LegalProceedingSerializer,
    AuctionSerializer,
    SalesInformationSerializer,
    ConnectionSerializer,
    MortgageAndDebtSerializer,
    SmallLeadSerializer,
    SmallOwnerSerializer,
    SmallPhoneSerializer,
    TaxLienSerializer,
    SmallPropertySerializer,
    FullPropertySerializer,
    DuplicateCheckSerializer

)
from rest_framework.response import Response
from .utils import check_priority, response_success, response_error, CustomPagination, standardize_address



class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    serializer_class = PropertySerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return SmallPropertySerializer
        elif self.action == 'retrieve':
            return FullPropertySerializer
        return PropertySerializer



class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return SmallOwnerSerializer
        return OwnerSerializer


class LegalProceedingViewSet(viewsets.ModelViewSet):
    queryset = LegalProceeding.objects.all().order_by("-id")
    serializer_class = LegalProceedingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all().order_by("-id")
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def retrieve_full(self, request, pk=None):
        instance = self.get_object()
        serializer = AuctionSerializer(instance)

        return response_success("Auction details retrieved successfully", serializer.data)


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

        existing_duplicate = DuplicateCheck.objects.filter(reformatted_address=standardized_address)
        if existing_duplicate.exists():
            duplicate_obj = existing_duplicate.last()
            is_important, priority_message = check_priority(
                source_name,
                duplicate_obj,
                is_auction
            )
            
            if is_important:
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


class ContactInformationViewSet(viewsets.ModelViewSet):
    queryset = ContactInformation.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ContactInformationSerializer
        return ContactInformationSerializer



class OwnershipViewSet(viewsets.ModelViewSet):
    queryset = Ownership.objects.all().order_by("-id")
    serializer_class = OwnershipSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination




