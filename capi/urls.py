
# from django.urls import path
# from .views import VideoModelViewSet

# urlpatterns = [
#     path('', VideoListCreateView.as_view(), name='video-list-create'),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoModelViewSet

router = DefaultRouter()
router.register('', VideoModelViewSet, basename='video')

urlpatterns = [
    path('', include(router.urls)),
]
