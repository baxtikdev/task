from django.db.models import Q
from rest_framework import filters


class OrderListFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = {}
        fields = ['client', 'waiter', 'courier', 'status', 'paymentStatus']

        for field in fields:
            param_value = request.query_params.get(field)
            if param_value in ['foods']:
                queryset = queryset.prefetch_related('foods')
            if param_value:
                filters[f'{field}__exact'] = param_value
        queryset = queryset.filter(**filters)

        return queryset