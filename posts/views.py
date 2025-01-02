from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from django.conf import settings
from .serializers import (PostSerializer, DetailPostSerializer, CommentSerializer, ListCommentSerializer,
                          DetailCommentSerializer, LikeSerializer)
from .models import Post, Comment, Like, PinnedPost, PinnedComment
from .permissions import IsAuthor
from .generics import PinnedItemAPIView


class ListCreatePostAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = "id"

    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Post.objects.list_with_pin_filter(PinnedPost).filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DetailPostAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DetailPostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]
    lookup_url_kwarg = "id"


class ListPostAPIView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return Post.objects.list_with_pin_filter(PinnedPost).filter(author_id=self.kwargs[self.lookup_url_kwarg])


class CommentAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return Comment.objects.list_with_pin_filter(PinnedComment).filter(post_id=self.kwargs[self.lookup_url_kwarg])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentSerializer

        return ListCommentSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user, post_id=self.kwargs[self.lookup_url_kwarg])


class DetailCommentAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DetailCommentSerializer
    queryset = Comment.objects.filter()
    permission_classes = (IsAuthenticated, IsAuthor,)
    lookup_url_kwarg = "id"


class ReplyAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "id"

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentSerializer

        return ListCommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(parent_id=self.kwargs[self.lookup_url_kwarg])

    def perform_create(self, serializer):
        parent_id = self.kwargs[self.lookup_url_kwarg]
        parent = Comment.objects.get(id=parent_id)

        return serializer.save(author=self.request.user, parent_id=parent_id,
                               post=parent.post)


class DetailReplyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DetailCommentSerializer
    queryset = Comment.objects.filter(parent__isnull=False)
    permission_classes = (IsAuthenticated, IsAuthor,)
    lookup_url_kwarg = "id"


class LikeAPIView(ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "id"

    def get_queryset(self):
        content_type = self.kwargs['target_type']
        return Like.objects.filter_for_object(model=content_type, object_id=self.kwargs[self.lookup_url_kwarg]).filter(
            is_liked=True)

    def get_object(self):
        # implemented for DRF permission handling compatibility, due to significant manipulations of the base queryset

        content_type = self.kwargs['target_type']
        object_id = self.kwargs[self.lookup_url_kwarg]
        user = self.request.user
        obj = Like.objects.get_object(content_type, object_id, user)
        self.check_object_permissions(self.request, obj)
        return obj

    def post(self, request, *args, **kwargs):
        content_type = self.kwargs['target_type']
        object_id = self.kwargs[self.lookup_url_kwarg]
        user = self.request.user
        obj = Like.objects.toggle_like_for(content_type, object_id, user)
        message = f"content {'liked' if obj.is_liked else 'unliked'}"
        return Response({"detail": message}, status=HTTP_200_OK)


class PinPostAPIView(PinnedItemAPIView):
    limit = settings.PINNED_POST_LIMIT
    queryset = PinnedPost.objects.all()
    object_model = Post
    pinned_object_model = PinnedPost


class PinCommentAPIView(PinnedItemAPIView):
    limit = settings.PINNED_COMMENT_LIMIT
    queryset = PinnedComment.objects.all()
    object_model = Comment
    pinned_object_model = PinnedComment
