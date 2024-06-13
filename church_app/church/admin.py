from django.contrib import admin
from .models import Event, Sermon, Member, Series, Scripture, RatingReview, Note

admin.site.register(Event)
admin.site.register(Sermon)
admin.site.register(Member)
admin.site.register(Series)
admin.site.register(Scripture)
admin.site.register(RatingReview)
admin.site.register(Note)

