import datetime

from django.db.models import ExpressionWrapper, Case, When, Value, BooleanField, Count, F
from rest_framework import generics, status
from rest_framework.response import Response

from api.order.filters import OrderListFilter
from api.order.serializers import OrderCreateSerializer, OrderListSerializer, OrderDetailSerializer, \
    OrderFoodSerializer, OrderFoodDetailSerializer
from api.paginator import CustomPagination
from api.permissions import IsClient, IsWaiter
from common.order.models import Order, OrderFood
from common.user.models import UserRole


class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsClient | IsWaiter]

    def create(self, request, *args, **kwargs):
        meals = request.data.pop('foods', [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_food_create = []

        totalAmount = 0
        for meal in meals:
            order_food_serializer = OrderFoodSerializer(data=meal)
            order_food_serializer.is_valid(raise_exception=True)
            order_food = OrderFood(**order_food_serializer.validated_data)
            order_food.orderPrice = order_food.food.price * order_food_serializer.validated_data.get('quantity')
            totalAmount += order_food.orderPrice
            order_food_create.append(order_food)
        order = serializer.save()
        if order_food_create:
            OrderFood.objects.bulk_create(order_food_create)
            order.foods.set(order_food_create)
            order.totalAmount = totalAmount
            res = OrderFood.objects.filter(isReady=False).count()
            mins = round(res / 4) * 5
            order.preparationTime = datetime.datetime.now() + datetime.timedelta(minutes=mins)
            distance = serializer.validated_data.get('distance')
            time = 0
            if distance:
                time = distance * 3
            order.deliveryTime = datetime.datetime.now() + datetime.timedelta(minutes=mins + time)
            order.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.select_related('client', 'waiter', 'courier').all().order_by('created_at')
    serializer_class = OrderListSerializer
    pagination_class = CustomPagination
    filter_backends = [OrderListFilter]
    permission_classes = [IsClient | IsWaiter]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.role == UserRole.CLIENT:
            queryset = queryset.filter(client=self.request.user)
        queryset = queryset.annotate(
            ready=ExpressionWrapper(
                Case(
                    When(foods__isReady=False, then=Value(False)),
                    default=Value(True),
                    output_field=BooleanField()
                ),
                output_field=BooleanField()
            )
        ).annotate(
            orderFoods=Count(F('foods'))
        )

        return queryset


class OrderRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.select_related('client', 'waiter', 'courier').all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsClient | IsWaiter]
    lookup_field = 'guid'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.role == UserRole.CLIENT:
            queryset = queryset.filter(client=self.request.user)
        queryset = queryset.annotate(
            ready=ExpressionWrapper(
                Case(
                    When(foods__isReady=False, then=Value(False)),
                    default=Value(True),
                    output_field=BooleanField()
                ),
                output_field=BooleanField()
            )
        ).annotate(
            orderFoods=Count(F('foods'))
        )

        return queryset


class OrderUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsClient | IsWaiter]
    lookup_field = 'guid'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.role == UserRole.CLIENT:
            queryset = queryset.filter(client=self.request.user)
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        meals = request.data.pop('foods', [])
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        order_food_create = []
        order_food_update = []

        totalAmount = 0
        for meal in meals:
            orderFood = OrderFood.objects.filter(id=meal.get('id'),
                                                 guid=meal.get('guid')).first()
            if orderFood is None:
                order_food_serializer = OrderFoodSerializer(data=meal)
                order_food_serializer.is_valid(raise_exception=True)
                order_food = OrderFood(**order_food_serializer.validated_data)
                order_food.orderPrice = order_food.food.price * order_food_serializer.validated_data.get('quantity')
                totalAmount += order_food.food.price * order_food_serializer.validated_data.get('quantity')
                order_food_create.append(order_food)
                continue

            order_food_serializer = OrderFoodSerializer(instance=orderFood, data=meal, partial=True)
            order_food_serializer.is_valid(raise_exception=True)
            orderFood.orderPrice = orderFood.food.price * order_food_serializer.validated_data.get('quantity')
            totalAmount += orderFood.food.price * order_food_serializer.validated_data.get('quantity')
            order_food_update.append(orderFood)

        order = serializer.save()
        if order_food_create:
            OrderFood.objects.bulk_create(order_food_create)
        if order_food_update:
            OrderFood.objects.bulk_update(order_food_create,
                                          fields=['food', 'orderPrice', 'quantity', 'description'])
        if order_food_create or order_food_update:
            order.foods.set(order_food_create + order_food_update)
        order.totalAmount = totalAmount
        order.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDestroyAPIView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    lookup_field = 'guid'
    permission_classes = [IsClient | IsWaiter]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.role == UserRole.CLIENT:
            queryset = queryset.filter(client=self.request.user)
        return queryset


class OrderFoodListAPIView(generics.ListAPIView):
    queryset = OrderFood.objects.select_related('food').all().order_by('created_at')
    serializer_class = OrderFoodDetailSerializer
    pagination_class = CustomPagination
    permission_classes = [IsWaiter]


class OrderFoodUpdateAPIView(generics.UpdateAPIView):
    queryset = OrderFood.objects.all()
    serializer_class = OrderFoodSerializer
    permission_classes = [IsWaiter]
    lookup_field = 'guid'
