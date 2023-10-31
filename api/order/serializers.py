from rest_framework import serializers

from api.auth.serializers import UserListSerializer
from api.food.serializers import FoodCreateSerializer
from common.order.models import Order, OrderFood


class OrderFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFood
        fields = ['id', 'guid', 'food', 'orderPrice', 'quantity', 'description']


class OrderFoodDetailSerializer(serializers.ModelSerializer):
    food = FoodCreateSerializer()

    class Meta:
        model = OrderFood
        fields = ['id', 'guid', 'food', 'orderPrice', 'quantity', 'description']


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'guid', 'client', 'waiter', 'courier', 'totalAmount', 'description', 'foods', 'status',
                  'paymentStatus', 'address', 'distance']


class OrderListSerializer(serializers.ModelSerializer):
    client = UserListSerializer()
    waiter = UserListSerializer()
    courier = UserListSerializer()
    ready = serializers.BooleanField(default=False)
    orderFoods = serializers.IntegerField(default=0)

    class Meta:
        model = Order
        fields = ['id', 'guid', 'client', 'waiter', 'courier', 'totalAmount', 'status', 'paymentStatus', 'address',
                  'distance', 'ready', 'orderFoods', 'preparationTime', 'deliveryTime']


class OrderDetailSerializer(serializers.ModelSerializer):
    client = UserListSerializer()
    waiter = UserListSerializer()
    courier = UserListSerializer()
    foods = OrderFoodDetailSerializer(many=True)
    ready = serializers.BooleanField(default=False)
    orderFoods = serializers.IntegerField(default=0)

    class Meta:
        model = Order
        fields = ['id', 'guid', 'client', 'waiter', 'courier', 'totalAmount', 'description', 'foods', 'status',
                  'paymentStatus', 'address', 'distance', 'ready', 'orderFoods', 'preparationTime', 'deliveryTime']
