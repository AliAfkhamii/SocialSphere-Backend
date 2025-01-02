from django.utils.functional import SimpleLazyObject
from django.contrib.auth import get_user_model

User = get_user_model()


# not yet included in MIDDLEWARES since there are still questions about its necessity to the project.
class ProfileMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: attach_lazy_profile(request.user))
        response = self.get_response(request)
        return response


def attach_lazy_profile(user):
    if not user.is_authenticated():
        return user

    def get_profile():
        if not hasattr(user, '_cached_profile'):
            user._cached_profile = User.objects.select_related('profile').get(pk=user.id).profile
        return user._cached_profile

    user.__class__.profile = property(get_profile)
    return user
