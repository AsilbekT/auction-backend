from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Property, Owner, LegalProceeding, Auction, SalesInformation, Connection, MortgageAndDebt, TaxLien
from .serializers import (
    PropertySerializer,
    OwnerSerializer,
    LegalProceedingSerializer,
    AuctionSerializer,
    SalesInformationSerializer,
    ConnectionSerializer,
    MortgageAndDebtSerializer,
    TaxLienSerializer,
    SmallPropertySerializer,
    FullPropertySerializer

)
from .utils import response_success, response_error, CustomPagination


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return SmallPropertySerializer
        if self.action == 'retrieve':
            return FullPropertySerializer
        return PropertySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)

        return response_success("Properties retrieved successfully", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response_success("Property details retrieved successfully", serializer.data)


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by("-id")
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


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
