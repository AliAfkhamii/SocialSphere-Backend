from rest_framework.permissions import BasePermission

from .models import Relation


def map_state(action):
    # we can skip 'request' as long as it's wrapped by 'follow'
    if action == 'follow':
        return Relation.RelationChoices.FOLLOWS
    elif action == 'block':
        return Relation.RelationChoices.BLOCKS


class NotIdentical(BasePermission):
    def has_permission(self, request, view):
        return request.user.id != view.kwargs.get(view.lookup_url_kwarg)


class NotBlocked(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not Relation.objects.filter(actor=obj, target=request.user,  # obj.user
                                           state=Relation.RelationChoices.BLOCKS).exists()


class StateNotAlreadySet(BasePermission):

    def has_object_permission(self, request, view, obj):
        new_state = map_state(request.action)
        return not Relation.objects.filter(actor=request.user, target=obj, state=new_state).exists()  # obj.user


class NotAlreadyBLocked(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not Relation.objects.filter(actor=request.user, target=obj,  # obj.user
                                           state=Relation.RelationChoices.BLOCKS).exists()


class IsRequested(BasePermission):
    def has_object_permission(self, request, view, obj):
        return Relation.objects.filter(actor=obj, target=request.user,  # obj.user
                                       state=Relation.RelationChoices.REQUESTED).exists()


AlreadyBlocked = ~ NotAlreadyBLocked

IsIdentical = ~ NotIdentical
