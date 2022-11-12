from django.urls import path
from rest_framework import routers

from ads.views import AdListView, AdDetailView, AdUploadImageView, AdCreateView, AdUpdateView, AdDeleteView
from users.views import LocationViewSet

router = routers.SimpleRouter()
router.register('location', LocationViewSet)

urlpatterns = [
    path("", AdListView.as_view(), name="all_ads"),
    path("<int:pk>/", AdDetailView.as_view(), name="ad_detail"),
    path("create/", AdCreateView.as_view(), name="create_ad"),
    path("<int:pk>/upload_image/", AdUploadImageView.as_view(), name="ad_upload_image"),
    path("<int:pk>/update/", AdUpdateView.as_view(), name="ad_update"),
    path("<int:pk>/delete/", AdDeleteView.as_view(), name="ad_delete"),
]

urlpatterns += router.urls
