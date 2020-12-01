from django.contrib import admin
from .models import Project, Tag

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'tag_list')

    def tag_list(self, obj):
        return ", ".join(obj.tags.all().values_list('name', flat=True))

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
