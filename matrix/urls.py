from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'articles', views.ListArticleViewSet)
router.register(r'scan', views.ScanViewSet)

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
]
