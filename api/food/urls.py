from django.urls import path

from api.food.views import FoodCreateAPIView, FoodListAPIView, FoodRetrieveAPIView, FoodUpdateAPIView, \
    FoodDestroyAPIView

urlpatterns = [
    path("-create/", FoodCreateAPIView.as_view(), name="food_create"),
    path("-list/", FoodListAPIView.as_view(), name="food_list"),
    path("-detail/<uuid:guid>/", FoodRetrieveAPIView.as_view(), name="food_detail"),
    path("-update/<uuid:guid>/", FoodUpdateAPIView.as_view(), name="food_update"),
    path("-delete/<uuid:guid>/", FoodDestroyAPIView.as_view(), name="food_delete"),
]