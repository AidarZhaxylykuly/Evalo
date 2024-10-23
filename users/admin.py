from django.contrib import admin
from .models import Profile, Follow, TestsFolder

admin.site.register(Profile)
admin.site.register(Follow)

@admin.register(TestsFolder)
class TestsFolderAdmin(admin.ModelAdmin):
    list_display = ['folder_name', 'owner']
    search_fields = ['folder_name', 'owner__username']
    autocomplete_fields = ['owner']