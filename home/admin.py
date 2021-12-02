from django.contrib import admin

from home.models import Announcement


class AnnouncementModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'hide_date')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(Announcement, AnnouncementModelAdmin)
