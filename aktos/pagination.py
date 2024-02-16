from rest_framework import pagination


class CustomCusorPagination(pagination.CursorPagination):
    ordering = "-date_created"
