from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, ArticleViewSet, BlogPostViewSet, ImageViewSet, VideoViewSet, DocumentViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'blogposts', BlogPostViewSet)
router.register(r'images', ImageViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'documents', DocumentViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

