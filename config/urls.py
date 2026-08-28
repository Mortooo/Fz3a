"""URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from home import views
from home import dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('volunteer/', views.volunteer_signup, name='volunteer_signup'),
    # Staff dashboard
    path('dashboard/', dashboard_views.dashboard_redirect, name='dashboard'),
    path('dashboard/settings/', dashboard_views.dashboard_settings, name='dashboard_settings'),
    path('dashboard/volunteers/', dashboard_views.dashboard_volunteers, name='dashboard_volunteers'),
    path('dashboard/volunteers/<int:pk>/status/', dashboard_views.dashboard_volunteer_status, name='dashboard_volunteer_status'),
    path('dashboard/volunteers/<int:pk>/delete/', dashboard_views.dashboard_volunteer_delete, name='dashboard_volunteer_delete'),
    path('dashboard/<slug:slug>/', dashboard_views.dashboard_section_list, name='dashboard_section_list'),
    path('dashboard/<slug:slug>/<int:pk>/edit/', dashboard_views.dashboard_section_edit, name='dashboard_section_edit'),
    path('dashboard/<slug:slug>/<int:pk>/delete/', dashboard_views.dashboard_section_delete, name='dashboard_section_delete'),
]

# Serve gallery files and the logo from the project root during development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
