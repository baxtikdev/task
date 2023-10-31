from django.contrib import admin

from common.order.models import Order, OrderFood

admin.site.register(OrderFood)
admin.site.register(Order)
