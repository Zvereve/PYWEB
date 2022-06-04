from rest_framework.permissions import BasePermission, SAFE_METHODS


class OnliAuthorEditNote(BasePermission):
    def has_object_permission(self, request, view, obj):
       ...