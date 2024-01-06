
from django.urls import path, include
from .views import *
urlpatterns = [
    path('', VideoUploadView.as_view(), name='upload_video'),
    path('api/', include('capi.urls')),
    path('search/', SubSearch.as_view(), name='sub_search'),
]