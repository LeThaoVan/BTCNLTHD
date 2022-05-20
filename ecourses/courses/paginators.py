from rest_framework import pagination


class RoutePaginator(pagination.PageNumberPagination):
    page_size = 4