from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение администраторам изменять данные.
    Неавторизованные пользователи не могут просматривать данные.
    Авторизованные пользователи могут только выполнять безопасные методы.
    """

    def has_permission(self, request, view):
        # Запретить доступ для неавторизованных пользователей
        if not request.user.is_authenticated:
            return False

        # Разрешить безопасные методы (GET, HEAD, OPTIONS) для всех аутентифицированных пользователей
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить изменения только администраторам
        return request.user.is_staff  # Проверяем is_staff