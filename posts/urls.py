from rest_framework import routers

from posts import views

router = routers.DefaultRouter()
router.register('posts', views.PostViewSet, "posts")

urlpatterns = []

urlpatterns += router.urls
