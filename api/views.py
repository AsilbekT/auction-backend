from rest_framework import viewsets, status
from django.db import transaction
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .models import  Email, Lead, Phone, Property, Owner, LegalProceeding, Auction, SalesInformation, Connection, MortgageAndDebt, TaxLien, DuplicateCheck, User
from .serializers import (
    CreateOrReadUserSerializer,UpdateOrDeleteUserSerializer,ListUserSerializer,
    ReadPropertySerializer,CreatePropertySerializer,UpdateOrDeletePropertySerializer,ListPropertySerializer,
    CreateOrReadTaxLienSerializer,UpdateOrDeleteTaxLienSerializer,ListTaxLienSerializer,
    CreateOrReadAuctionSerializer,UpdateOrDeleteAuctionSerializer,ListAuctionSerializer,
    CreateOrReadDuplicateCheckSerializer,UpdateOrDeleteDuplicateCheckSerializer,ListDuplicateCheckSerializer,
    ReadOwnerSerializer,CreateOwnerSerializer,UpdateOrDeleteOwnerSerializer,ListOwnerSerializer,
    CreateOrReadEmailSerializer,UpdateOrDeleteEmailSerializer,ListEmailSerializer,
    CreateOrReadPhoneSerializer,UpdateOrDeletePhoneSerializer,ListPhoneSerializer,
    CreateOrReadMortgageAndDebtSerializer,UpdateOrDeleteMortgageAndDebtSerializer,ListMortgageAndDebtSerializer,
    CreateOrReadLegalProceedingSerializer,UpdateOrDeleteLegalProceedingSerializer,ListLegalProceedingSerializer,
    CreateOrReadConnectionSerializer,UpdateOrDeleteConnectionSerializer,ListConnectionSerializer,
    CreateOrReadSalesInformationSerializer,UpdateOrDeleteSalesInformationSerializer,ListSalesInformationSerializer,
    CreateLeadSerializer,ReadLeadSerializer,UpdateOrDeleteLeadSerializer,ListLeadSerializer,
)
from rest_framework.response import Response
from .utils import response_success, response_error, CustomPagination, standardize_address

class QueryParamFilterMixin:
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

        sort = query_params.get('sort', None)
        if sort:
            sort_fields = sort.split(',')
            queryset = queryset.order_by(*sort_fields)

        return queryset

class PropertyViewSet(QueryParamFilterMixin,viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create']:
            return CreatePropertySerializer
        elif self.action in ['retrieve']:
            return ReadPropertySerializer
        elif self.action in ['update','delete'] :
            return UpdateOrDeletePropertySerializer
        return ListPropertySerializer

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



class OwnerViewSet(QueryParamFilterMixin,viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateOwnerSerializer
        elif self.action in ['retrieve']:
            return ReadOwnerSerializer
        elif self.action in ['update','delete'] :
            return UpdateOrDeleteOwnerSerializer
        return ListOwnerSerializer


class LegalProceedingViewSet(QueryParamFilterMixin,viewsets.ModelViewSet):
    queryset = LegalProceeding.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create','retrieve']:
            return CreateOrReadLegalProceedingSerializer
        elif self.action in ['update','delete'] :
            return UpdateOrDeleteLegalProceedingSerializer
        return ListLegalProceedingSerializer

class UserViewSet(QueryParamFilterMixin,viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create','retrieve']:
            return CreateOrReadUserSerializer
        elif self.action in ['update','delete'] :
            return UpdateOrDeleteUserSerializer
        return ListUserSerializer

class AuctionViewSet(QueryParamFilterMixin,viewsets.ModelViewSet):
    queryset = Auction.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create','retrieve']:
            return CreateOrReadAuctionSerializer
        elif self.action in ['update','delete'] :
            return UpdateOrDeleteAuctionSerializer
        return ListAuctionSerializer

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


class SalesInformationViewSet(QueryParamFilterMixin,viewsets.ModelViewSet):
    queryset = SalesInformation.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create','retrieve']:
            return CreateOrReadSalesInformationSerializer
        elif self.action in ['update','delete'] :
            return UpdateOrDeleteSalesInformationSerializer
        return ListSalesInformationSerializer


class ConnectionViewSet(QueryParamFilterMixin,viewsets.ModelViewSet):
    queryset = Connection.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create','retrieve']:
            return CreateOrReadConnectionSerializer
        elif self.action in ['update','delete'] :
            return UpdateOrDeleteConnectionSerializer
        return ListConnectionSerializer

class MortgageAndDebtViewSet(QueryParamFilterMixin,viewsets.ModelViewSet):
    queryset = MortgageAndDebt.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create','retrieve']:
            return CreateOrReadMortgageAndDebtSerializer
        elif self.action in ['update','delete'] :
            return UpdateOrDeleteMortgageAndDebtSerializer
        return ListMortgageAndDebtSerializer


class TaxLienViewSet(QueryParamFilterMixin,viewsets.ModelViewSet):
    queryset = TaxLien.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create','retrieve']:
            return CreateOrReadTaxLienSerializer
        elif self.action in ['update','delete'] :
            return UpdateOrDeleteTaxLienSerializer
        return ListTaxLienSerializer


class DuplicateCheckViewSet(QueryParamFilterMixin,viewsets.ModelViewSet):
    queryset = DuplicateCheck.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create','retrieve']:
            return CreateOrReadDuplicateCheckSerializer
        elif self.action in ['update','delete'] :
            return UpdateOrDeleteDuplicateCheckSerializer
        return ListDuplicateCheckSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created, message = self.perform_create(serializer)
        print(created, message)
        if not created:
            return response_error("error", message, http_status=status.HTTP_409_CONFLICT)
        
        serializer.save()
        return response_success("Success", serializer.data)

    def perform_create(self, serializer):
        standardized_address = standardize_address(serializer.validated_data.get("reformatted_address"))
        source_name = serializer.validated_data.get("source_name")
        is_auction = serializer.validated_data.get("is_auction")
        
        if standardized_address is None:
            return False, "Invalid address format"

        existing_duplicate = DuplicateCheck.objects.filter(reformatted_address=standardized_address,is_auction=is_auction)
        if existing_duplicate.exists():
            duplicate_obj = existing_duplicate.last()
            if duplicate_obj.source_name == source_name :
                return False , "it should be update"
        return True , "new address created"


class LeadViewSet(QueryParamFilterMixin,viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateLeadSerializer
        elif self.action in ['retrieve']:
            return ReadLeadSerializer
        elif self.action in ['update','delete']:
            return UpdateOrDeleteLeadSerializer
        return ListLeadSerializer
    

    def create(self, request, *args, **kwargs):
        data = request.data

        # Pop data from request
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
        current_user_id = request.user.id

        lead_is_new = True
        
        with transaction.atomic() :

            if duplicate_check_data:
                duplicate_check_data["reformatted_address"] = standardize_address(duplicate_check_data["reformatted_address"])
                duplicate_serializer = CreateOrReadDuplicateCheckSerializer(data=duplicate_check_data)
                duplicate_serializer.is_valid(raise_exception=True)
                duplicate_view = DuplicateCheckViewSet()
                success, _ = duplicate_view.perform_create(duplicate_serializer)
                if not success:
                    duplicate_check = DuplicateCheck.objects.filter(
                        reformatted_address=duplicate_check_data['reformatted_address'],
                        source_name=duplicate_check_data['source_name'],
                        is_auction=duplicate_check_data['is_auction']
                    ).last()
                    lead_is_new = False
                else :
                    duplicate_check = duplicate_serializer.save()
            else :
                raise ValidationError("Duplicate check data should not be empty")

            if property_data:
                if lead_is_new :
                    property_serializer = CreatePropertySerializer(data=property_data)
                    property_serializer.is_valid(raise_exception=True)
                    property = property_serializer.save(duplicate_check = duplicate_check)
                else :
                    property = Property.objects.filter(duplicate_check=duplicate_check).last()

                if legalproceeding_data:
                    legalproceeding_serializer = CreateOrReadLegalProceedingSerializer(data=legalproceeding_data)
                    legalproceeding_serializer.is_valid(raise_exception=True)
                    try :
                        legalproceeding_serializer.save(property=property)
                    except ValidationError as e:
                        print(f"Lead validation error: {e}")

                if mortgageanddebt_data:
                    mortgageanddebt_serializer = CreateOrReadMortgageAndDebtSerializer(data=mortgageanddebt_data)
                    mortgageanddebt_serializer.is_valid(raise_exception=True)
                    mortgageanddebt_serializer.save(property=property)

                if taxlien_data:
                    taxlien_serializer = CreateOrReadTaxLienSerializer(data=taxlien_data)
                    taxlien_serializer.is_valid(raise_exception=True)
                    taxlien_serializer.save(property=property)

            if lead_is_new:
                lead_data = {
                    **data,
                    "created_by": current_user_id,
                }
                lead_serializer = CreateLeadSerializer(data=lead_data)
                lead_serializer.is_valid(raise_exception=True)
                lead = lead_serializer.save(property=property)
            else :
                lead = Lead.objects.filter(property=property).last()

            if owner_data:
                owner_serializer = CreateOwnerSerializer(data=owner_data)
                owner_serializer.is_valid(raise_exception=True)
                owner = owner_serializer.save(lead=lead)

                for phone in phones_data:
                    phone_serializer = CreateOrReadPhoneSerializer(data=phone)
                    phone_serializer.is_valid(raise_exception=True)
                    phone_serializer.save(owner=owner)

                for email in emails_data:
                    email_serializer = CreateOrReadEmailSerializer(data=email)
                    email_serializer.is_valid(raise_exception=True)
                    email_serializer.save(owner=owner)

                for connection in connections_data:
                    connection_serializer = CreateOrReadConnectionSerializer(data=connection)
                    connection_serializer.is_valid(raise_exception=True)
                    connection_serializer.save(owner=owner)


            if auction_data:
                auction_serializer = CreateOrReadAuctionSerializer(data=auction_data)
                auction_serializer.is_valid(raise_exception=True)
                auction_serializer.save(lead=lead)

            if salesInformation_data:
                sales_information_serializer = CreateOrReadSalesInformationSerializer(data=salesInformation_data)
                sales_information_serializer.is_valid(raise_exception=True)
                sales_information_serializer.save(lead=lead)

            if lead_is_new and lead:
                return Response(lead_serializer.data, status=status.HTTP_201_CREATED)
            
            lead.updated_at = now()
            lead.save()
            return Response(CreateLeadSerializer(lead).data, status=status.HTTP_200_OK)



class PhoneViewSet(QueryParamFilterMixin,viewsets.ModelViewSet):
    queryset = Phone.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create','retrieve']:
            return CreateOrReadPhoneSerializer
        elif self.action in ['update','delete']:
            return UpdateOrDeletePhoneSerializer
        return ListPhoneSerializer

class EmailViewSet(QueryParamFilterMixin,viewsets.ModelViewSet):
    queryset = Email.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['create','retrieve']:
            return CreateOrReadEmailSerializer
        elif self.action in ['update','delete']:
            return UpdateOrDeleteEmailSerializer
        return ListEmailSerializer






