from django.urls import path

from .views import *
from .models import Post, Comment

urlpatterns = [
    path('posts/', ListCreatePostAPIView.as_view()),
    path('posts/<int:id>/', DetailPostAPIView.as_view()),
    path('profiles/<int:id>/posts/', ListPostAPIView.as_view()),

    path('posts/<int:id>/comments/', CommentAPIView.as_view()),
    path('comments/<int:id>/', DetailCommentAPIView.as_view()),

    path('comments/<int:id>/replies/', ReplyAPIView.as_view()),
    path('replies/<int:id>/', DetailCommentAPIView.as_view()),

    path('posts/<int:id>/likes/', LikeAPIView.as_view(), {'target_type': Post}),
    path('comments/<int:id>/likes/', LikeAPIView.as_view(), {'target_type': Comment}),

    path('posts/<int:id>/toggle_pin/', PinPostAPIView.as_view()),
    path('comments/<int:id>/toggle_pin/', PinCommentAPIView.as_view())
]
