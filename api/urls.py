from django.urls import path
from .views import category_list_create_view, CategoryDetailAPIView, PostAPIView, PostDetailAPIView, AuthListCreateView, AuthRetriveUpdateDestroyAPIView
from .views import LoginAPIView, LogoutAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("category/", category_list_create_view, name="cat-list-create"),
    path("category/detail/<slug:slug>", CategoryDetailAPIView.as_view(), name="cat-detail"),
    path("post/", PostAPIView.as_view(), name="post-list"),
    path("post/detail/<slug:slug>/", PostDetailAPIView.as_view(), name="post-detail-list"),
    path("auth/", AuthListCreateView.as_view(), name="auth-list"),
    path("auth/detail/<int:pk>/", AuthRetriveUpdateDestroyAPIView.as_view(), name="auth-detail")
]
