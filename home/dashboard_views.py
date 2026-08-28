from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
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
    ('values', 'قيم المبادرة', 'fa-solid fa-heart'),
    ('fields', 'مجالات العمل', 'fa-solid fa-hand-holding-heart'),
    ('projects', 'مشاريعنا', 'fa-solid fa-moon'),
    ('gallery', 'معرض الأثر', 'fa-solid fa-images'),
    ('donations', 'طرق المساهمة', 'fa-solid fa-coins'),
]


def _base_context(request, active):
    return {
        'active_tab': active,
        'section_tabs': SECTION_TABS,
        'new_volunteers': VolunteerApplication.objects.filter(status='new').count(),
        'volunteers_total': VolunteerApplication.objects.count(),
        'can_logout': True,
    }


@staff_member_required(login_url='admin:login')
def dashboard_redirect(request):
    return redirect('dashboard_settings')


# ---------------------------------------------------------------------------
# Site Settings
# ---------------------------------------------------------------------------

@staff_member_required(login_url='admin:login')
def dashboard_settings(request):
    settings = SiteSettings.objects.first()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم حفظ إعدادات الموقع بنجاح.')
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
            'verbose': 'قيمة',
            'urlslug': 'values',
            'tabs_key': 'values',
        },
        'fields': {
            'model': FieldOfWork,
            'form': FieldOfWorkForm,
            'verbose': 'مجال عمل',
            'urlslug': 'fields',
            'tabs_key': 'fields',
        },
        'projects': {
            'model': Project,
            'form': ProjectForm,
            'verbose': 'مشروع',
            'urlslug': 'projects',
            'tabs_key': 'projects',
        },
        'gallery': {
            'model': GalleryItem,
            'form': GalleryItemForm,
            'verbose': 'عنصر معرض',
            'urlslug': 'gallery',
            'tabs_key': 'gallery',
        },
        'donations': {
            'model': DonationMethod,
            'form': DonationMethodForm,
            'verbose': 'طريقة مساهمة',
            'urlslug': 'donations',
            'tabs_key': 'donations',
        },
    }


def _row_for(section_slug, obj):
    """Return display dict per section for the generic list table."""
    slug = section_slug
    if slug == 'values':
        return {
            'العنوان': obj.title,
            'الأيقونة': f"<i class='{obj.icon}'></i>",
            'الترتيب': obj.order,
        }
    if slug == 'fields':
        return {'العنوان': obj.title, 'اللون': obj.color, 'الترتيب': obj.order}
    if slug == 'projects':
        return {'العنوان': obj.title, 'الشارة': obj.badge, 'الترتيب': obj.order}
    if slug == 'gallery':
        kind = 'صورة' if obj.media_type == 'photo' else 'فيديو'
        return {'العنوان': obj.title, 'النوع': kind, 'الترتيب': obj.order, 'ظاهر': 'نعم' if obj.active else 'لا'}
    if slug == 'donations':
        cat = 'حسابات مصرفية' if obj.category == 'bank' else 'عبر الرصيد'
        return {'الاسم': obj.name, 'الرقم': obj.number, 'الفئة': cat, 'الترتيب': obj.order}
    return {'العنوان': str(obj)}


# Cache of (info, list_view, edit_view, delete_view) per slug.
_section_cache = {}


def _get_section(slug):
    if slug not in _section_cache:
        info = _model_tabs()[slug]
        model = info['model']
        form_cls = info['form']

        @staff_member_required(login_url='admin:login')
        def section_list(request, slug=slug, model=model, form_cls=form_cls, info=info):
            context = _base_context(request, slug)
            context['section'] = info
            if request.method == 'POST':
                form = form_cls(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, f'تمت إضافة {info["verbose"]} بنجاح.')
                    return redirect('dashboard_section_list', slug)
            else:
                form = form_cls()
            objects = list(model.objects.all())
            context['form'] = form
            context['objects'] = objects
            context['row_headers'] = list(_row_for(slug, objects[0]).keys()) if objects else []
            context['rows'] = [(o.pk, _row_for(slug, o)) for o in objects]
            return render(request, 'home/dashboard/section_list.html', context)

        @staff_member_required(login_url='admin:login')
        def section_edit(request, pk, slug=slug, model=model, form_cls=form_cls, info=info):
            obj = get_object_or_404(model, pk=pk)
            if request.method == 'POST':
                form = form_cls(request.POST, request.FILES, instance=obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'تم حفظ التعديلات بنجاح.')
                    return redirect('dashboard_section_list', slug)
            else:
                form = form_cls(instance=obj)
            context = _base_context(request, slug)
            context['section'] = info
            context['form'] = form
            context['object'] = obj
            return render(request, 'home/dashboard/section_edit.html', context)

        @staff_member_required(login_url='admin:login')
        @require_POST
        def section_delete(request, pk, slug=slug, model=model, info=info):
            obj = get_object_or_404(model, pk=pk)
            obj.delete()
            messages.success(request, 'تم الحذف بنجاح.')
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

@staff_member_required(login_url='admin:login')
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


@staff_member_required(login_url='admin:login')
@require_POST
def dashboard_volunteer_status(request, pk):
    obj = get_object_or_404(VolunteerApplication, pk=pk)
    new_status = request.POST.get('status', '')
    valid = dict(VolunteerApplication.Status.choices)
    if new_status not in valid:
        return JsonResponse({'ok': False, 'error': 'حالة غير صالحة'}, status=400)
    obj.status = new_status
    obj.save(update_fields=['status'])
    return JsonResponse({'ok': True, 'status': obj.get_status_display()})


@staff_member_required(login_url='admin:login')
@require_POST
def dashboard_volunteer_delete(request, pk):
    obj = get_object_or_404(VolunteerApplication, pk=pk)
    obj.delete()
    messages.success(request, 'تم حذف الطلب.')
    return redirect('dashboard_volunteers')
