from django.urls import path, include
from rest_framework import routers

from posts import views

router = routers.DefaultRouter()
router.register('posts', views.PostViewSet, "posts")
router.register('image', views.ImageViewSet, "image")

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls
