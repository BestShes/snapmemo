from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from user.views import UserViewSet, UserLoginViewSet, UserLogoutViewSet

router = routers.DefaultRouter()
router.register(
    r'user',
    UserViewSet
),
router.register(
    r'login',
    UserLoginViewSet
)
router.register(
    r'logout',
    UserLogoutViewSet
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls, namespace='api')),
]
