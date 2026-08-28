from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import (
    SiteSettingsForm,
    CoreValueForm,
    FieldOfWorkForm,
    ProjectForm,
    GalleryItemForm,
    DonationMethodForm,
)
from .models import (
    SiteSettings,
    CoreValue,
    FieldOfWork,
    Project,
    GalleryItem,
    DonationMethod,
    VolunteerApplication,
)

SECTION_TABS = [
    ('values', 'ظ‚ظٹظ… ط§ظ„ظ…ط¨ط§ط¯ط±ط©', 'fa-solid fa-heart'),
    ('fields', 'ظ…ط¬ط§ظ„ط§طھ ط§ظ„ط¹ظ…ظ„', 'fa-solid fa-hand-holding-heart'),
    ('projects', 'ظ…ط´ط§ط±ظٹط¹ظ†ط§', 'fa-solid fa-moon'),
    ('gallery', 'ظ…ط¹ط±ط¶ ط§ظ„ط£ط«ط±', 'fa-solid fa-images'),
    ('donations', 'ط·ط±ظ‚ ط§ظ„ظ…ط³ط§ظ‡ظ…ط©', 'fa-solid fa-coins'),
]


def _base_context(request, active):
    return {
        'active_tab': active,
        'section_tabs': SECTION_TABS,
        'new_volunteers': VolunteerApplication.objects.filter(status='new').count(),
        'volunteers_total': VolunteerApplication.objects.count(),
        'can_logout': True,
    }


# ---------------------------------------------------------------------------
# Login (styled dashboard login form)
# ---------------------------------------------------------------------------

def dashboard_login(request):
    if request.user.is_staff:
        return redirect(request.GET.get('next') or '/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff and user.is_active:
            login(request, user)
            return redirect(request.POST.get('next') or '/dashboard/')
        error = 'ط¨ظٹط§ظ†ط§طھ ط§ظ„ط¯ط®ظˆظ„ ط؛ظٹط± طµط­ظٹط­ط©طŒ ط£ظˆ ط§ظ„ط­ط³ط§ط¨ ط؛ظٹط± ظ…ط®ظˆظ‘ظ„ ظ„ظ„ظˆط­ط© ط§ظ„طھط­ظƒظ….'
    context = {
        'error': error,
        'next': request.GET.get('next') or request.POST.get('next') or '/dashboard/',
    }
    return render(request, 'home/dashboard/login.html', context)


@staff_member_required(login_url='dashboard_login')
def dashboard_redirect(request):
    return redirect('dashboard_settings')


# ---------------------------------------------------------------------------
# Site Settings
# ---------------------------------------------------------------------------

@staff_member_required(login_url='dashboard_login')
def dashboard_settings(request):
    settings = SiteSettings.objects.first()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'طھظ… ط­ظپط¸ ط¥ط¹ط¯ط§ط¯ط§طھ ط§ظ„ظ…ظˆظ‚ط¹ ط¨ظ†ط¬ط§ط­.')
            return redirect('dashboard_settings')
    else:
        form = SiteSettingsForm(instance=settings)
    context = _base_context(request, 'settings')
    context.update({'form': form, 'settings_obj': settings})
    return render(request, 'home/dashboard/settings.html', context)


# ---------------------------------------------------------------------------
# Generic content-section factory
# ---------------------------------------------------------------------------

def _model_tabs():
    """Return softcoded model info to build tabs."""
    return {
        'values': {
            'model': CoreValue,
            'form': CoreValueForm,
            'verbose': 'ظ‚ظٹظ…ط©',
            'urlslug': 'values',
            'tabs_key': 'values',
        },
        'fields': {
            'model': FieldOfWork,
            'form': FieldOfWorkForm,
            'verbose': 'ظ…ط¬ط§ظ„ ط¹ظ…ظ„',
            'urlslug': 'fields',
            'tabs_key': 'fields',
        },
        'projects': {
            'model': Project,
            'form': ProjectForm,
            'verbose': 'ظ…ط´ط±ظˆط¹',
            'urlslug': 'projects',
            'tabs_key': 'projects',
        },
        'gallery': {
            'model': GalleryItem,
            'form': GalleryItemForm,
            'verbose': 'ط¹ظ†طµط± ظ…ط¹ط±ط¶',
            'urlslug': 'gallery',
            'tabs_key': 'gallery',
        },
        'donations': {
            'model': DonationMethod,
            'form': DonationMethodForm,
            'verbose': 'ط·ط±ظٹظ‚ط© ظ…ط³ط§ظ‡ظ…ط©',
            'urlslug': 'donations',
            'tabs_key': 'donations',
        },
    }


def _row_for(section_slug, obj):
    """Return display dict per section for the generic list table."""
    slug = section_slug
    if slug == 'values':
        return {
            'ط§ظ„ط¹ظ†ظˆط§ظ†': obj.title,
            'ط§ظ„ط£ظٹظ‚ظˆظ†ط©': f"<i class='{obj.icon}'></i>",
            'ط§ظ„طھط±طھظٹط¨': obj.order,
        }
    if slug == 'fields':
        return {'ط§ظ„ط¹ظ†ظˆط§ظ†': obj.title, 'ط§ظ„ظ„ظˆظ†': obj.color, 'ط§ظ„طھط±طھظٹط¨': obj.order}
    if slug == 'projects':
        return {'ط§ظ„ط¹ظ†ظˆط§ظ†': obj.title, 'ط§ظ„ط´ط§ط±ط©': obj.badge, 'ط§ظ„طھط±طھظٹط¨': obj.order}
    if slug == 'gallery':
        kind = 'طµظˆط±ط©' if obj.media_type == 'photo' else 'ظپظٹط¯ظٹظˆ'
        return {'ط§ظ„ط¹ظ†ظˆط§ظ†': obj.title, 'ط§ظ„ظ†ظˆط¹': kind, 'ط§ظ„طھط±طھظٹط¨': obj.order, 'ط¸ط§ظ‡ط±': 'ظ†ط¹ظ…' if obj.active else 'ظ„ط§'}
    if slug == 'donations':
        cat = 'ط­ط³ط§ط¨ط§طھ ظ…طµط±ظپظٹط©' if obj.category == 'bank' else 'ط¹ط¨ط± ط§ظ„ط±طµظٹط¯'
        return {'ط§ظ„ط§ط³ظ…': obj.name, 'ط§ظ„ط±ظ‚ظ…': obj.number, 'ط§ظ„ظپط¦ط©': cat, 'ط§ظ„طھط±طھظٹط¨': obj.order}
    return {'ط§ظ„ط¹ظ†ظˆط§ظ†': str(obj)}


# Cache of (info, list_view, edit_view, delete_view) per slug.
_section_cache = {}


def _get_section(slug):
    if slug not in _section_cache:
        info = _model_tabs()[slug]
        model = info['model']
        form_cls = info['form']

        @staff_member_required(login_url='dashboard_login')
        def section_list(request, slug=slug, model=model, form_cls=form_cls, info=info):
            context = _base_context(request, slug)
            context['section'] = info
            if request.method == 'POST':
                form = form_cls(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, f'طھظ…طھ ط¥ط¶ط§ظپط© {info["verbose"]} ط¨ظ†ط¬ط§ط­.')
                    return redirect('dashboard_section_list', slug)
            else:
                form = form_cls()
            objects = list(model.objects.all())
            context['form'] = form
            context['objects'] = objects
            context['row_headers'] = list(_row_for(slug, objects[0]).keys()) if objects else []
            context['rows'] = [(o.pk, _row_for(slug, o)) for o in objects]
            return render(request, 'home/dashboard/section_list.html', context)

        @staff_member_required(login_url='dashboard_login')
        def section_edit(request, pk, slug=slug, model=model, form_cls=form_cls, info=info):
            obj = get_object_or_404(model, pk=pk)
            if request.method == 'POST':
                form = form_cls(request.POST, request.FILES, instance=obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'طھظ… ط­ظپط¸ ط§ظ„طھط¹ط¯ظٹظ„ط§طھ ط¨ظ†ط¬ط§ط­.')
                    return redirect('dashboard_section_list', slug)
            else:
                form = form_cls(instance=obj)
            context = _base_context(request, slug)
            context['section'] = info
            context['form'] = form
            context['object'] = obj
            return render(request, 'home/dashboard/section_edit.html', context)

        @staff_member_required(login_url='dashboard_login')
        @require_POST
        def section_delete(request, pk, slug=slug, model=model, info=info):
            obj = get_object_or_404(model, pk=pk)
            obj.delete()
            messages.success(request, 'طھظ… ط§ظ„ط­ط°ظپ ط¨ظ†ط¬ط§ط­.')
            return redirect('dashboard_section_list', slug)

        _section_cache[slug] = (info, section_list, section_edit, section_delete)
    return _section_cache[slug]


def dashboard_section_list(request, slug):
    if slug not in _model_tabs():
        return redirect('dashboard_settings')
    return _get_section(slug)[1](request)


def dashboard_section_edit(request, slug, pk):
    if slug not in _model_tabs():
        return redirect('dashboard_settings')
    return _get_section(slug)[2](request, pk)


def dashboard_section_delete(request, slug, pk):
    if slug not in _model_tabs():
        return redirect('dashboard_settings')
    return _get_section(slug)[3](request, pk)


# ---------------------------------------------------------------------------
# Volunteers
# ---------------------------------------------------------------------------

@staff_member_required(login_url='dashboard_login')
def dashboard_volunteers(request):
    context = _base_context(request, 'volunteers')
    applications = VolunteerApplication.objects.all()
    status_q = request.GET.get('status', '')
    if status_q in dict(VolunteerApplication.Status.choices):
        applications = applications.filter(status=status_q)
    search_q = request.GET.get('q', '').strip()
    if search_q:
        applications = applications.filter(
            Q(full_name__icontains=search_q)
            | Q(phone__icontains=search_q)
            | Q(email__icontains=search_q)
            | Q(city__icontains=search_q)
            | Q(interest__icontains=search_q)
        )
    context['applicants'] = applications
    context['status_choices'] = VolunteerApplication.Status.choices
    context['current_status_filter'] = status_q
    context['search_q'] = search_q
    return render(request, 'home/dashboard/volunteers.html', context)


@staff_member_required(login_url='dashboard_login')
@require_POST
def dashboard_volunteer_status(request, pk):
    obj = get_object_or_404(VolunteerApplication, pk=pk)
    new_status = request.POST.get('status', '')
    valid = dict(VolunteerApplication.Status.choices)
    if new_status not in valid:
        return JsonResponse({'ok': False, 'error': 'ط­ط§ظ„ط© ط؛ظٹط± طµط§ظ„ط­ط©'}, status=400)
    obj.status = new_status
    obj.save(update_fields=['status'])
    return JsonResponse({'ok': True, 'status': obj.get_status_display()})


@staff_member_required(login_url='dashboard_login')
@require_POST
def dashboard_volunteer_delete(request, pk):
    obj = get_object_or_404(VolunteerApplication, pk=pk)
    obj.delete()
    messages.success(request, 'طھظ… ط­ط°ظپ ط§ظ„ط·ظ„ط¨.')
    return redirect('dashboard_volunteers')
