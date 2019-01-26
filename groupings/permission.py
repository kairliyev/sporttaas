from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    """
    This custom permission will only allow owners of
    object to edit and view
    """

    def has_object_permission(self, request, view, obj):
        return obj.admin == request.user


class IsMemberOnly(permissions.BasePermission):
    """
    This custom permission will only allow owners of
    object to edit and view
    """

    def has_object_permission(self, request, view, obj):
        check = False
        for i in obj.members.all():
            if i == request.user:
                check = True
        return check