from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EventViewSet, SeriesViewSet, ScriptureViewSet,
    SermonViewSet, RatingReviewViewSet, NoteViewSet, MemberViewSet,
    VersionedEventViewSet, DefaultVersioningViewSet
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'series', SeriesViewSet, basename='series')
router.register(r'scriptures', ScriptureViewSet, basename='scripture')
router.register(r'sermons', SermonViewSet, basename='sermon')
router.register(r'rating-reviews', RatingReviewViewSet, basename='rating_review')
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'members', MemberViewSet, basename='member')

# Optionally, register versioned viewsets
router.register(r'versioned-events', VersionedEventViewSet, basename='versioned_event')
router.register(r'default-versioning', DefaultVersioningViewSet, basename='default_versioning')

urlpatterns = [
    path('', include(router.urls)),
]

# Additional URL configurations can be added as needed

