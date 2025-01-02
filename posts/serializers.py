from rest_framework import serializers
from generic_relations.relations import GenericRelatedField

from .models import *


class PinSerializer:
    is_pinned = serializers.SerializerMethodField(method_name='is_pinned')

    def is_pinned(self, obj):
        return PinnedPost.objects.filter(post=obj).exists()


class PostSerializer(serializers.ModelSerializer):
    is_pinned = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'image',
            'file',
            'is_pinned',
        ]
        read_only_field = ['is_pinned', ]

    def get_is_pinned(self, obj):
        return PinnedPost.objects.filter(post=obj).exists()


class DetailPostSerializer(serializers.ModelSerializer):
    is_pinned = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["author", "likes", "is_pinned"]

    def get_is_pinned(self, obj):
        return PinnedPost.objects.filter(post=obj).exists()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']


class ListCommentSerializer(serializers.ModelSerializer):
    has_reply = serializers.SerializerMethodField()
    is_pinned = serializers.SerializerMethodField(method_name='get_is_pinned')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created', 'is_pinned', 'has_reply', 'parent']

    def get_has_reply(self, obj):
        return obj.replies.exists()

    def get_is_pinned(self, obj):
        return PinnedComment.objects.filter(comment=obj).exists()


class DetailCommentSerializer(serializers.ModelSerializer):
    has_reply = serializers.SerializerMethodField()
    is_pinned = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['author', 'post', 'content', 'created', 'is_pinned', 'parent', 'has_reply']
        read_only_fields = ['author', 'post', 'created', 'is_pinned', 'parent', ]

    def get_has_reply(self, obj):
        return obj.replies.exists()

    def get_is_pinned(self, obj):
        return PinnedComment.objects.filter(comment=obj).exists()


class LikeSerializer(serializers.ModelSerializer):
    liked_object = GenericRelatedField({
        Post: serializers.PrimaryKeyRelatedField(queryset=Post.objects.all()),
        Comment: serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())
    },
        source='content_object'
    )

    class Meta:
        model = Like
        fields = ["user", "liked_object", "created", ]
        read_only_fields = fields
