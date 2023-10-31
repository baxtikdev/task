from rest_framework import generics

from api.food.serializers import FoodCreateSerializer, FoodListSerializer, FoodDetailSerializer
from api.paginator import CustomPagination
from api.permissions import IsWaiter
from common.food.models import Food


class FoodCreateAPIView(generics.CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodCreateSerializer
    permission_classes = [IsWaiter]


class FoodListAPIView(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodListSerializer
    pagination_class = CustomPagination


class FoodRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodDetailSerializer
    lookup_field = 'guid'


class FoodUpdateAPIView(generics.UpdateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodCreateSerializer
    permission_classes = [IsWaiter]
    lookup_field = 'guid'


class FoodDestroyAPIView(generics.DestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodCreateSerializer
    permission_classes = [IsWaiter]
    lookup_field = 'guid'
