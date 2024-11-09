from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsRoomMember(BasePermission):
    def has_object_permission(self, request, view, obj):  
        return request.user in obj.members.all() or request.user == obj.owner

class IsRoomOwner(BasePermission) :
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner