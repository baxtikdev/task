from rest_framework.permissions import BasePermission

from common.user.models import UserRole


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(request.user and request.user.is_active
                    and request.user.role == UserRole.ADMIN)


class IsWaiter(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(
            request.user and request.user.is_active and
            request.user.role == UserRole.WAITER or
            request.user.role == UserRole.ADMIN)


class IsClient(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(
            request.user and request.user.is_active and
            request.user.role == UserRole.CLIENT or
            request.user.role == UserRole.ADMIN)
