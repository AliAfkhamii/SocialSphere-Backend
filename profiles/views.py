from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin, GenericViewSet
from rest_framework.status import HTTP_200_OK

from .serializers import UserProfileSerializer, UserPrivateProfileSerializer
from .permissions import *
from .models import Profile, Relation
from rest_framework.generics import RetrieveUpdateDestroyAPIView

User = get_user_model()


# class ProfileViewSet(NoCreateModelViewSet):
#     queryset = Profile.objects.all()
#     permission_classes = [IsAuthenticated, NotBlocked]
#
#     def get_serializer_class(self):
#             user = self.request.user.profile
#             target = self.get_object()
#             if user.is_private and not Relation.objects.is_following(user, target):
#                 return PrivateProfileSerializer
#
#             return ProfileSerializer
#
#     def list(self, request, *args, **kwargs):
#         return Response({"detail": "this endpoint is not available"}, status=HTTP_404_NOT_FOUND)
#
#
#

class ProfileAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(User, id=self.request.user.id)

        self.check_object_permissions(self.request, self.request.user)

        return obj


class ProfileDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    lookup_url_kwarg = "id"
    permission_classes = [IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        user = self.request.user
        target = self.get_object()
        if user.profile.is_private and not Relation.objects.is_following(user, target):
            return UserPrivateProfileSerializer

        return UserProfileSerializer


class ActionViewSet(GenericViewSet, ViewSetMixin):
    queryset = User.objects.all()

    # serializer_class = ProfileSerializer  # redundant

    @action(methods=['POST'], detail=True,
            permission_classes=[IsAuthenticated, NotIdentical, NotBlocked, StateNotAlreadySet, NotAlreadyBLocked])
    def follow(self, request, *args, **kwargs):
        user = self.get_object()
        Relation.objects.follow(request.user, user)
        return Response({"message": f"user '{user.username}' has been followed"}, status=HTTP_200_OK)

    @action(methods=['POST'], detail=True,
            permission_classes=[IsAuthenticated, NotIdentical, StateNotAlreadySet])
    def block(self, request, *args, **kwargs):
        user = self.get_object()
        Relation.objects.block(request.user, user)
        return Response({"message": f"user '{user.username}' has been blocked"}, status=HTTP_200_OK)

    @action(methods=['POST'], detail=True,
            permission_classes=[IsAuthenticated, NotIdentical, NotBlocked, NotAlreadyBLocked])
    def unfollow(self, request, *args, **kwargs):
        user = self.get_object()
        Relation.objects.unfollow(request.user, user)
        return Response({"message": f"user '{user.username}' has been unfollowed"}, status=HTTP_200_OK)

    @action(methods=['POST'], detail=True,
            permission_classes=[IsAuthenticated, AlreadyBlocked])
    def unblock(self, request, *args, **kwargs):
        user = self.get_object()
        Relation.objects.unblock(request.user, user)
        return Response({"message": f"user '{user.username}' has been unblocked"}, status=HTTP_200_OK)

    @action(methods=['POST'], detail=True,
            permission_classes=[IsAuthenticated, NotBlocked, NotAlreadyBLocked])
    def undo_request(self, request, *args, **kwargs):
        user = self.get_object()
        Relation.objects.undo_request(request.user, user)
        return Response({"message": f"follow request to user '{user.username}' has been undone"}, status=HTTP_200_OK)

    @action(methods=['POST'], detail=True,
            permission_classes=[IsAuthenticated, IsRequested])
    def accept(self, request, *args, **kwargs):
        user = self.get_object()
        Relation.objects.accept(request.user, user)
        return Response({"message": f"follow request accepted"}, status=HTTP_200_OK)

    @action(methods=['POST'], detail=True,
            permission_classes=[IsAuthenticated, IsRequested])
    def decline(self, request, *args, **kwargs):
        user = self.get_object()
        Relation.objects.decline(request.user, user)
        return Response({"message": f"follow request declined"}, status=HTTP_200_OK)
