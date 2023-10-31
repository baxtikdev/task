from django.db import models

from common.user.base import BaseModel


class Food(BaseModel):
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="foodImages", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
