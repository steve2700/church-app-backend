from django.contrib import admin
from .models import Event, Series, Scripture, Sermon, RatingReview, Note, Member

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'status', 'organizer')
    search_fields = ('title', 'organizer__username')

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    search_fields = ('title',)

@admin.register(Scripture)
class ScriptureAdmin(admin.ModelAdmin):
    list_display = ('book', 'chapter', 'verse')
    search_fields = ('book', 'chapter', 'verse')

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'speaker')
    search_fields = ('title', 'speaker__username')

@admin.register(RatingReview)
class RatingReviewAdmin(admin.ModelAdmin):
    list_display = ('sermon', 'user', 'rating', 'date_created')
    search_fields = ('sermon__title', 'user__username')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('sermon', 'user', 'timestamp')
    search_fields = ('sermon__title', 'user__username')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'date_joined')
    search_fields = ('user__username', 'phone_number')

