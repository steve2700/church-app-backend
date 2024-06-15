from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.versioning import NamespaceVersioning, AcceptHeaderVersioning
from .models import Event, Series, Scripture, Sermon, RatingReview, Note, Member
from .serializers import (
    EventSerializer, SeriesSerializer, ScriptureSerializer,
    SermonSerializer, RatingReviewSerializer, NoteSerializer, MemberSerializer
)

# Pagination configuration
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Event CRUD operations.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'date']  # Example of using DjangoFilterBackend
    ordering_fields = ['date']
    ordering = ['date']
    pagination_class = StandardResultsSetPagination
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class SeriesViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Series CRUD operations.
    """
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['start_date']
    ordering = ['start_date']
    pagination_class = StandardResultsSetPagination
    authentication_classes = [TokenAuthentication, SessionAuthentication]

class ScriptureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Scripture CRUD operations.
    """
    queryset = Scripture.objects.all()
    serializer_class = ScriptureSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['book', 'chapter']  # Example of using DjangoFilterBackend
    search_fields = ['book', 'chapter']  # Example of using SearchFilter
    pagination_class = StandardResultsSetPagination
    authentication_classes = [TokenAuthentication, SessionAuthentication]

class SermonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Sermon CRUD operations.
    """
    queryset = Sermon.objects.all()
    serializer_class = SermonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['series']  # Example of using DjangoFilterBackend
    ordering_fields = ['date']
    ordering = ['date']
    pagination_class = StandardResultsSetPagination
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(speaker=self.request.user)

class RatingReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling RatingReview CRUD operations.
    """
    queryset = RatingReview.objects.all()
    serializer_class = RatingReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    authentication_classes = [TokenAuthentication, SessionAuthentication]

class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Note CRUD operations.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    authentication_classes = [TokenAuthentication, SessionAuthentication]

class MemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Member CRUD operations.
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def perform_create(self, serializer):
        # Automatically create a user associated with the member
        user_serializer = serializer.validated_data.pop('user')
        user = User.objects.create(**user_serializer)
        serializer.save(user=user)

    def perform_update(self, serializer):
        # Update both member and associated user details
        instance = self.get_object()
        user_serializer = serializer.validated_data.pop('user')
        user = instance.user
        user.username = user_serializer.get('username', user.username)
        user.email = user_serializer.get('email', user.email)
        user.save()

        serializer.save()

    def get_queryset(self):
        # Optionally filter queryset based on request user role or other criteria
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user=self.request.user)

# Versioning example
class VersionedEventViewSet(EventViewSet):
    """
    Versioned Event ViewSet with API versioning.
    """
    versioning_class = NamespaceVersioning

    # Override methods or add version-specific behaviors as needed

# Alternatively, you can version all viewsets by setting a default versioning scheme
class DefaultVersioningViewSet(viewsets.ModelViewSet):
    """
    Default versioned ViewSet.
    """
    versioning_class = AcceptHeaderVersioning

    # Define viewset logic as usual

    def list(self, request, *args, **kwargs):
        # Custom logic for list method
        return super().list(request, *args, **kwargs)

# Include other viewsets with versioning as needed

