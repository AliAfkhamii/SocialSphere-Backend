from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Exists, OuterRef


class ModelPinManager(models.Manager):

    def list_with_pin_filter(self, item_model):
        lookup_field = {
            f"{self.model.__name__}_id".lower(): OuterRef('pk')
        }
        return self.annotate(
            is_pinned=Exists(
                item_model.objects.filter(**lookup_field)
            )
        ).order_by('-is_pinned', '-created')


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=300)
    image = models.ImageField(null=True)
    file = models.FileField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation('Like')

    objects = ModelPinManager()


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='replies')
    likes = GenericRelation('Like')

    objects = ModelPinManager()

    def is_reply(self):
        return self.parent is not None


class LikeManager(models.Manager):

    def filter_for_object(self, model, object_id):
        content_type = ContentType.objects.get_for_model(model)
        return self.filter(content_type=content_type, object_id=object_id)

    def get_object(self, model, object_id, user):
        return self.filter_for_object(model, object_id).filter(user=user).first()

    def toggle_like_for(self, model, object_id, user):
        content_type = ContentType.objects.get_for_model(model)
        obj, _ = self.get_or_create(content_type_id=content_type.id, object_id=object_id, user=user)
        obj.is_liked = not obj.is_liked

        obj.save(update_fields=['is_liked'])
        return obj


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.BigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)

    objects = LikeManager()

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        unique_together = ('content_type', 'object_id', 'user')


class PinManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)


class PinnedComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    comment = models.OneToOneField('Comment', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    objects = PinManager()


class PinnedPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    objects = PinManager()
