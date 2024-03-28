from django.contrib import admin
from .models import Author, Quote, Tag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "fullname",
        "born_date",
        "born_location",
        "created_at",
        "is_active",
    )
    search_fields = ("fullname", "born_date", "created_at")
    list_filter = ("is_active",)
    actions = ["deactivate", "activate"]
    ordering = ("id",)

    def deactivate(self, request, queryset):
        self.message_user(request, f"Authors deactivated")
        queryset.update(is_active=False)

    deactivate.short_description = "Deactivate author"

    def activate(self, request, queryset):
        self.message_user(request, f"Authors activated")
        queryset.update(is_active=True)

    activate.short_description = "Activate author"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_filter = []
    actions = None
    ordering = ("id",)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("id", "quote", "author", "get_tags", "created_at")
    search_fields = ("quote", "author", "get_tags")
    list_filter = ["author"]
    ordering = ("id",)

    def get_tags(self, obj):
        return ", ".join([p.name for p in obj.tags.all()])

    get_tags.short_description = "Tags"
