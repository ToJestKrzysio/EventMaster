from django.contrib import admin

from home.models import Announcement


class AnnouncementModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'hide_date')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Announcement, AnnouncementModelAdmin)
