from django.urls import path
from users.views import (
    CreateUserView,
    ListUsersView,
    UpdateUserView,
    DeleteUserView, LoginUserView, RetrieveUserView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("users/", ListUsersView.as_view(), name="list_users"),
    path("users/<int:pk>/", RetrieveUserView.as_view(), name="retrieve_user"),
    path("users/<int:pk>/update/", UpdateUserView.as_view(), name="update_user"),
    path("users/<int:pk>/delete/", DeleteUserView.as_view(), name="delete_user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

app_name = "users"
