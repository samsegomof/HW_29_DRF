from django.urls import path

from users.views import UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView

urlpatterns = [
    path("", UserListView.as_view(), name="all_users"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("create/", UserCreateView.as_view(), name="create_user"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update_user"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="delete_user"),
]
