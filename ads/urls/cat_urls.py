from django.urls import path

from ads.views import CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

urlpatterns = [
    path("", CategoryListView.as_view(), name="all_categories"),
    path("<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("create/", CategoryCreateView.as_view(), name="create_category"),
    path("update/<int:pk>/", CategoryUpdateView.as_view(), name="update_category"),
    path("delete/<int:pk>/", CategoryDeleteView.as_view(), name="delete_category"),
]
