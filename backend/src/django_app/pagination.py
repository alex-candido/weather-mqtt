from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10 # Default page size
    page_size_query_param = 'page_size' # Allow client to set page size
    max_page_size = 100 # Maximum page size allowed

    def get_paginated_response(self, data):
        return Response({
            'total_count': self.page.paginator.count,
            'count': len(data),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
