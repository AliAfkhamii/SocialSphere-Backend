from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from .permissions import IsAuthor


class PinnedItemAPIView(APIView):
    limit = None
    queryset = None
    object_model = None
    pinned_object_model = None
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        return self.queryset.all()

    def get_limit(self):
        return self.limit

    def get_pinned_count(self):
        queryset = self.get_queryset()
        return queryset.filter(user=self.request.user).count()

    def post(self, request, *args, **kwargs):
        pinned_count = self.get_pinned_count()

        if pinned_count >= self.get_limit():
            raise serializers.ValidationError("pin limit has been exceeded")

        obj = get_object_or_404(self.object_model, pk=self.kwargs.get('id'))
        self.check_object_permissions(request, obj)

        lookup_fields = {
            "user": request.user,
            f"{self.object_model.__name__}_id".lower(): obj.id
        }

        pinned_obj = self.pinned_object_model.objects.filter(**lookup_fields).first()

        if pinned_obj:
            pinned_obj.is_active = not pinned_obj.is_active
            pinned_obj.save(update_fields=['is_active'])
            message = "pinned" if pinned_obj.is_active else "unpinned"

        else:
            lookup_fields = {
                "user": request.user,
                f"{self.object_model.__name__}_id".lower(): self.kwargs.get('id')
            }

            self.pinned_object_model.objects.create(**lookup_fields)
            message = "pinned"

        return Response(f"{self.object_model.__name__} {message}", status=HTTP_200_OK)
