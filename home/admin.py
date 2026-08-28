from django.contrib import admin

from .models import SiteSettings, CoreValue, FieldOfWork, Project, GalleryItem, DonationMethod


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'tagline', 'hashtag')
    verbose_name = "إعدادات الموقع"


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(FieldOfWork)
class FieldOfWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'order', 'active')
    list_filter = ('media_type', 'active')
    list_editable = ('order', 'active')


@admin.register(DonationMethod)
class DonationMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'category', 'order')
    list_filter = ('category',)
    list_editable = ('order',)
