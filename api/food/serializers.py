from rest_framework import serializers

from common.food.models import Food


class FoodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'guid', 'title', 'photo', 'price', 'description']


class FoodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'guid', 'title', 'photo', 'price']


class FoodDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'guid', 'title', 'photo', 'price', 'description']
