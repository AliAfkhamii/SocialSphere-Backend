from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ActionViewSet, ProfileAPIView, ProfileDetailAPIView

router = SimpleRouter()
router.register('profile', ActionViewSet)

urlpatterns = [
    path('profile/me/', ProfileAPIView.as_view()),
    path('profile/<int:id>/', ProfileDetailAPIView.as_view()),
    path('', include(router.urls)),
]
