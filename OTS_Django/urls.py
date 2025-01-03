"""
URL configuration for OTS_Django project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('inventory/', include('inventory.urls')),
    path('production/', include('production.urls')),
    path('quality/', include('quality.urls')),  # Add quality URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
