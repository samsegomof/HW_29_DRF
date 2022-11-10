from django.urls import path

from ads.views import AdListView, AdDetailView, AdUploadImageView, AdCreateView

urlpatterns = [
    path("", AdListView.as_view(), name="all_ads"),
    path("<int:pk>/", AdDetailView.as_view(), name="ad_detail"),
    path("create/", AdCreateView.as_view(), name="create_ad"),
    path("<int:pk>/upload_image/", AdUploadImageView.as_view(), name="ad_upload_image"),
]
