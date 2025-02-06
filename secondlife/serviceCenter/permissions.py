from rest_framework import permissions


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

