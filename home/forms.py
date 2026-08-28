from django import forms

from .models import (
    VolunteerApplication,
    SiteSettings,
    CoreValue,
    FieldOfWork,
    Project,
    GalleryItem,
    DonationMethod,
)

LIGHT_INPUT = 'w-full rounded-xl bg-white border border-slate-300 px-4 py-2.5 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20'
LIGHT_TEXTAREA = 'w-full rounded-xl bg-white border border-slate-300 px-4 py-2.5 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20'
LIGHT_SELECT = 'w-full rounded-xl bg-white border border-slate-300 px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20'


class VolunteerApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ['full_name', 'phone', 'email', 'city', 'interest', 'availability', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full rounded-xl bg-slate-800 border border-slate-700 px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500', 'placeholder': 'الاسم الكامل', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'w-full rounded-xl bg-slate-800 border border-slate-700 px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500', 'placeholder': 'رقم الجوال / واتساب', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'w-full rounded-xl bg-slate-800 border border-slate-700 px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500', 'placeholder': 'البريد الإلكتروني (اختياري)'}),
            'city': forms.TextInput(attrs={'class': 'w-full rounded-xl bg-slate-800 border border-slate-700 px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500', 'placeholder': 'المدينة (اختياري)'}),
            'interest': forms.Textarea(attrs={'rows': 3, 'class': 'w-full rounded-xl bg-slate-800 border border-slate-700 px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500', 'placeholder': 'مجالات الاهتمام أو الخبرات (مثال: العمل الميداني، التواصل، التصوير...)'}),
            'availability': forms.TextInput(attrs={'class': 'w-full rounded-xl bg-slate-800 border border-slate-700 px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500', 'placeholder': 'أوقات التوفر (اختياري)'}),
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'w-full rounded-xl bg-slate-800 border border-slate-700 px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500', 'placeholder': 'رسالة إضافية (اختياري)'}),
        }


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'tagline', 'hashtag',
            'hero_headline', 'hero_intro',
            'story_badge', 'story_headline', 'story_paragraphs',
            'mission_title', 'mission_text',
            'vision_title', 'vision_text',
            'whatsapp_link', 'facebook_link', 'donation_name',
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'tagline': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'hashtag': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'hero_headline': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'hero_intro': forms.Textarea(attrs={'class': LIGHT_TEXTAREA, 'rows': 3}),
            'story_badge': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'story_headline': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'story_paragraphs': forms.Textarea(attrs={'class': LIGHT_TEXTAREA, 'rows': 6}),
            'mission_title': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'mission_text': forms.Textarea(attrs={'class': LIGHT_TEXTAREA, 'rows': 4}),
            'vision_title': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'vision_text': forms.Textarea(attrs={'class': LIGHT_TEXTAREA, 'rows': 4}),
            'whatsapp_link': forms.URLInput(attrs={'class': LIGHT_INPUT}),
            'facebook_link': forms.URLInput(attrs={'class': LIGHT_INPUT}),
            'donation_name': forms.TextInput(attrs={'class': LIGHT_INPUT}),
        }


class CoreValueForm(forms.ModelForm):
    class Meta:
        model = CoreValue
        fields = ['title', 'description', 'icon', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'description': forms.Textarea(attrs={'class': LIGHT_TEXTAREA, 'rows': 2}),
            'icon': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'order': forms.NumberInput(attrs={'class': LIGHT_INPUT}),
        }


class FieldOfWorkForm(forms.ModelForm):
    class Meta:
        model = FieldOfWork
        fields = ['title', 'description', 'footer_note', 'icon', 'color', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'description': forms.Textarea(attrs={'class': LIGHT_TEXTAREA, 'rows': 3}),
            'footer_note': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'icon': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'color': forms.Select(attrs={'class': LIGHT_SELECT}, choices=[('rose', 'Rose'), ('amber', 'Amber'), ('blue', 'Blue')]),
            'order': forms.NumberInput(attrs={'class': LIGHT_INPUT}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'badge', 'icon', 'gradient', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'description': forms.Textarea(attrs={'class': LIGHT_TEXTAREA, 'rows': 3}),
            'badge': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'icon': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'gradient': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'order': forms.NumberInput(attrs={'class': LIGHT_INPUT}),
        }


class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['media_type', 'title', 'subtitle', 'file', 'direct_url', 'order', 'active']
        widgets = {
            'media_type': forms.Select(attrs={'class': LIGHT_SELECT}),
            'title': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'subtitle': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'direct_url': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'order': forms.NumberInput(attrs={'class': LIGHT_INPUT}),
            'active': forms.CheckboxInput(attrs={'class': 'w-5 h-5 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500'}),
        }


class DonationMethodForm(forms.ModelForm):
    class Meta:
        model = DonationMethod
        fields = ['name', 'number', 'category', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'number': forms.TextInput(attrs={'class': LIGHT_INPUT}),
            'category': forms.Select(attrs={'class': LIGHT_SELECT}),
            'order': forms.NumberInput(attrs={'class': LIGHT_INPUT}),
        }
