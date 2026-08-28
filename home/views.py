from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import VolunteerApplicationForm
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
        'volunteer_form': VolunteerApplicationForm(),
    }
    return render(request, 'home/index.html', context)


@require_POST
def volunteer_signup(request):
    form = VolunteerApplicationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'ok': True})
    errors = {
        field: [str(e) for e in errs]
        for field, errs in form.errors.items()
    }
    return JsonResponse({'ok': False, 'errors': errors}, status=400)
