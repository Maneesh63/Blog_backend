from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import CategorViewSet, BlogCreateView
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()

router.register(r'categories', CategorViewSet, basename='category')
urlpatterns = [
    path('', include(router.urls)),
    path('posts/', BlogCreateView.as_view(), name='blog-create'),
    path('posts/update/<uuid:post_id>/', BlogCreateView.as_view(), name='blog-update')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)