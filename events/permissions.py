from rest_framework.permissions import BasePermission


class UserIsOwnerEvents(BasePermission):

    def has_object_permission(self, request, view, event):
        return request.user.id == event.user.id
