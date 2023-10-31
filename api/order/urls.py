from django.urls import path

from api.order.views import OrderCreateAPIView, OrderListAPIView, OrderRetrieveAPIView, OrderUpdateAPIView, \
    OrderDestroyAPIView, OrderFoodUpdateAPIView, OrderFoodListAPIView

urlpatterns = [
    path("-create/", OrderCreateAPIView.as_view(), name="Order_create"),
    path("-list/", OrderListAPIView.as_view(), name="Order_list"),
    path("-detail/<uuid:guid>/", OrderRetrieveAPIView.as_view(), name="Order_detail"),
    path("-update/<uuid:guid>/", OrderUpdateAPIView.as_view(), name="Order_update"),
    path("-delete/<uuid:guid>/", OrderDestroyAPIView.as_view(), name="Order_delete"),
    path("-food-update/<uuid:guid>/", OrderFoodUpdateAPIView.as_view(), name="Order_food_update"),
    path("-food-list/", OrderFoodListAPIView.as_view(), name="Order_food_list"),
]