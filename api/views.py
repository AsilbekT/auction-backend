from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from .models import Property
from .serializers import PropertySerializer
from .utils import response_success, response_error, CustomPagination

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        """
        Handle GET requests for listing properties with pagination.
        Returns a standardized response with paginated data.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            return response_success("Data fetched successfully", paginated_data)

        serializer = self.get_serializer(queryset, many=True)
        return response_success("Data fetched successfully", {"data": serializer.data, "pagination": None})

    def create(self, request, *args, **kwargs):
        """
        Handle POST requests for creating a new property.
        Returns a standardized response with the created property details.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_success("Property created successfully.", serializer.data)
        return response_error("Invalid data.", serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Handle PUT/PATCH requests for updating an existing property.
        Returns a standardized response with the updated property details.
        """
        try:
            property_instance = self.get_object()
        except NotFound:
            return response_error("Property not found.", None, status.HTTP_404_NOT_FOUND)

        partial = request.method == "PATCH"  # Allow partial updates for PATCH requests
        serializer = self.get_serializer(property_instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return response_success("Property updated successfully.", serializer.data)
        return response_error("Invalid data.", serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Handle DELETE requests for deleting a property.
        Returns a standardized response upon successful deletion.
        """
        try:
            property_instance = self.get_object()
            property_instance.delete()
            return response_success("Property deleted successfully.", None)
        except NotFound:
            return response_error("Property not found.", None, status.HTTP_404_NOT_FOUND)
