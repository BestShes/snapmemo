from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers

from memo.views import CategoryViewSet, MemoViewSet
from snapmemo import settings
from user.views import UserViewSet

router = routers.DefaultRouter()
router.register(
    r'user',
    UserViewSet
),
router.register(
    r'category',
    CategoryViewSet
)
router.register(
    r'memo',
    MemoViewSet
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls, namespace='api')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
