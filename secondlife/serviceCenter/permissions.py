from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrCreateUser(permissions.BasePermission):
    """
    Разрешение, позволяющее администратору создавать мастеров,
    а всем остальным пользователям — создавать обычных пользователей.
    """

    def has_permission(self, request, view):
        # Разрешить доступ всем пользователям для создания
        if request.method == 'POST':
            return True

        # Запретить доступ для всех остальных методов
        return request.user.is_staff


#Разрешение для админа и пользователей
class IsUserOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.user_type in ['user', 'admin'] or
            request.user.is_staff  # Для администратора
        )