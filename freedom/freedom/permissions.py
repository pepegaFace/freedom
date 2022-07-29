from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    edit_methods = ("GET", "PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser and request.method not in self.edit_methods:
            return True

        return False


class IsManager(permissions.BasePermission):

    edit_methods = ("GET", "PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'Manager' or request.user.is_superuser:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.role == 'Manager' or request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser or request.user.role == 'Manager' and request.method not in self.edit_methods:
            return True

        return False


class IsAdminCRM(permissions.BasePermission):

    edit_methods = ("GET", "PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'AdminCRM' or request.user.is_superuser:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.role == 'AdminCRM':
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser or request.user.role == 'AdminCRM' and request.method not in self.edit_methods:
            return True

        return False


class IsSelf(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.pk == user.pk
