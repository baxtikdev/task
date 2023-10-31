from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    path("auth", include('api.auth.urls')),
    path("food", include('api.food.urls')),
    path("order", include('api.order.urls')),
]
