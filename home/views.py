from django.shortcuts import render

from .models import (
    SiteSettings,
    CoreValue,
    FieldOfWork,
    Project,
    GalleryItem,
    DonationMethod,
)


def index(request):
    settings = SiteSettings.objects.first()
    context = {
        'settings': settings,
        'values': CoreValue.objects.all(),
        'fields': FieldOfWork.objects.all(),
        'projects': Project.objects.all(),
        'gallery_photos': GalleryItem.objects.filter(media_type='photo', active=True),
        'gallery_videos': GalleryItem.objects.filter(media_type='video', active=True),
        'bank_methods': DonationMethod.objects.filter(category='bank'),
        'mobile_methods': DonationMethod.objects.filter(category='mobile'),
    }
    return render(request, 'home/index.html', context)
