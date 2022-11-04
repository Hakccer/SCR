from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("signup", signup, name="signup"),
    path("login", login, name="login"),
    path("verify_user", verify_user, name="verify"),
    path("get_token", TokenObtainPairView.as_view(), name="Jwt Login"),
    path("ref_token", TokenRefreshView.as_view(), name="refresh"),
    path("all_posts", AllPosts.as_view(), name="all_posts"),
    path("single/<int:pk>", SinglePost, name="Single_Post"),
    path("handle_like", handle_liking, name="handlikes"),
    path("comment", CommentApi.as_view(), name="Comments")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
