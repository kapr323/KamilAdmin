from django.contrib.admin import ModelAdmin


class KamilAdmin(ModelAdmin):
    @staticmethod
    def cleanup_description(modeladmin, request, queryset):
        queryset.update(description=None)