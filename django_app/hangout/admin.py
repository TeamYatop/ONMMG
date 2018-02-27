from django.contrib import admin

from hangout.models import Hangout, Tag


class HangoutAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'latitude', 'longitude']


admin.site.register(Hangout, HangoutAdmin)
admin.site.register(Tag)
