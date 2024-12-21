from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    picture = models.FileField(upload_to='profile pictures')
    phone_number = models.CharField(max_length=30)
    bio = models.TextField()
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.user

    @property
    def is_private(self):
        return self.private

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


class RelationQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class AllRelationManager(models.Manager):
    def get_queryset(self):
        return RelationQuerySet(self.model, using=self._db)

    def follow(self, actor, target):
        relation, created = self.get_or_create(actor=actor, target=target)
        STATE_FIELD = 'state'
        IS_ACTIVE_FIELD = 'is_active'
        update_fields = [STATE_FIELD]

        if relation.is_active and relation.state == relation.RelationChoices.REQUESTED:
            raise PermissionDenied("a follow request has already been sent to this user")

        if not created and not relation.is_active:
            relation.is_active = True
            update_fields.append(IS_ACTIVE_FIELD)

        relation.state = relation.RelationChoices.REQUESTED if target.is_private \
            else relation.RelationChoices.FOLLOWS

        relation.save(update_fields=update_fields)
        return relation

    def block(self, actor, target):
        relation, _ = self.get_or_create(actor=actor, target=target)
        relation.state = relation.RelationChoices.BLOCKS
        relation.save(update_fields=['state'])
        self._perform_block_effects(actor=target, target=actor)
        return relation

    def _perform_block_effects(self, actor, target):
        relation = self.filter(actor=actor, target=target, is_active=True).first()

        if relation and relation.state != relation.RelationChoices.BLOCKS:
            relation.is_active = False

        relation.save(update_fields=['is_active'])
        return relation


class RelationManager(AllRelationManager):
    def get_queryset(self):
        return RelationQuerySet(self.model, using=self._db).active()

    def unfollow(self, actor, target):
        relation = self.filter(actor=actor, target=target).first()
        if not relation or relation.state == relation.RelationChoices.REQUESTED:
            raise ValidationError('you are not following this user')

        relation.is_active = False
        relation.save(update_fields='is_active')
        return relation

    def unblock(self, actor, target):
        relation = self.filter(actor=actor, target=target).first()
        relation.is_active = False
        relation.save(update_fields='is_active')
        return relation

    def undo_request(self, actor, target):
        relation = self.filter(actor=actor, target=target, state=self.model.RelationChoices.REQUESTED).first()

        if not relation:
            raise ValidationError('no active follow request exists.')

        relation.is_active = False
        relation.save(update_fields='is_active')
        return relation

    def accept(self, actor, target):
        relation = self.filter(actor=target, target=actor).first()
        relation.state = relation.RelationChoices.FOLLOWS
        relation.save(update_fields='state')
        return relation

    def decline(self, actor, target):
        relation = self.filter(actor=target, target=actor).first()
        relation.is_active = False
        relation.save(update_fields='is_active')
        return relation

    def followers(self, profile):
        return self.filter(target=profile, state=self.model.RelationChoices.FOLLOWS)

    def followings(self, profile):
        return self.filter(actor=profile, state=self.model.RelationChoices.FOLLOWS)

    def mutual_followers(self, profile, mutual_profile):
        return self.filter(actor=profile, target=mutual_profile, state=self.model.RelationChoices.FOLLOWS)

    def requests(self, profile):
        return self.filter(target=profile, state=self.model.RelationChoices.REQUESTED)

    def blocklist(self, profile):
        return self.filter(actor=profile, state=self.model.RelationChoices.BLOCKS)

    def is_following(self, actor, target):
        return self.filter(actor=actor, target=target, state=self.model.RelationChoices.FOLLOWS).exists()


class Relation(models.Model):
    class RelationChoices(models.TextChoices):
        FOLLOWS = 'FOLLOWS', 'FOLLOWS'
        BLOCKS = 'BLOCKS', 'BLOCKS'
        REQUESTED = 'REQUESTED', 'REQUESTED'

    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actions')
    target = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='targeted')
    state = models.CharField(max_length=10, choices=RelationChoices.choices)
    date_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = RelationManager()
    all_objects = AllRelationManager()

    class Meta:
        unique_together = [
            ('actor', 'target'),
        ]
        default_manager_name = 'objects'

        verbose_name = _('relation')
        verbose_name_plural = _('relations')
