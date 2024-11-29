from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'error': False,
            'message': 'Data fetched successfully',
            'data': {
                'results': data,
                'pagination': {
                    'count': self.page.paginator.count,
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                }
            }
        })


def response_success(message, data):
    return Response({
        'error': False,
        'message': message,
        'data': data
    }, status=status.HTTP_200_OK)

def response_error(message, errors, http_status):
    return Response({
        'error': True,
        'message': message,
        'details': errors
    }, status=http_status)
