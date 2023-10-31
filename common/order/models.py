from django.db import models

from common.food.models import Food
from common.user.base import BaseModel
from common.user.models import User


class OrderFood(BaseModel):
    food = models.ForeignKey(Food, related_name='foodOrderFood', on_delete=models.CASCADE)
    orderPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    isReady = models.BooleanField(default=False)

    @property
    def amount(self):
        return self.food.price * self.quantity

    def __str__(self):
        return f"Order Food #{self.id} {self.food.title}"


class OrderStatus(models.IntegerChoices):
    WAITING = 1, "WAITING"
    RECEIVED = 2, "RECEIVED"
    IN_PROCESS = 3, "IN_PROCESS"
    IN_WAY = 4, "IN_WAY"
    DELIVERED = 5, "DELIVERED"
    CANCELLED = 6, "CANCELLED"


class OrderPaymentStatus(models.IntegerChoices):
    WAITING = 1, "WAITING"
    CANCELLED = 2, "CANCELLED"
    PAID = 3, "PAID"


class Order(BaseModel):
    client = models.ForeignKey(User, related_name='clientOrder', on_delete=models.CASCADE)
    waiter = models.ForeignKey(User, related_name='waiterOrder', on_delete=models.SET_NULL, null=True, blank=True)
    courier = models.ForeignKey(User, related_name='courierOrder', on_delete=models.SET_NULL, null=True, blank=True)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(null=True, blank=True)
    foods = models.ManyToManyField(OrderFood, related_name='foodsOrder', blank=True)
    status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.WAITING)
    paymentStatus = models.IntegerField(choices=OrderPaymentStatus.choices, default=OrderPaymentStatus.WAITING)
    address = models.CharField(max_length=255)
    preparationTime = models.TimeField(null=True, blank=True)
    deliveryTime = models.TimeField(null=True, blank=True)
    distance = models.IntegerField(default=0)


    def __str__(self):
        return f"Order #{self.id} {self.totalAmount}"
