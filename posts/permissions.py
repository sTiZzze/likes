from rest_framework.permissions import BasePermission


class PostPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action in ['check', 'like', 'report', 'top']:
            return obj == request.user or request.user.is_staff
        elif view.action in ['list']:
            return request.user.is_staff
        return False
