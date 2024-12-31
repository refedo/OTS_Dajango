from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('home/', views.dashboard, name='home'),  # Alias for dashboard
    
    # Material URLs
    path('materials/', views.material_list, name='material_list'),
    path('materials/create/', views.material_create, name='material_create'),
    path('materials/<int:pk>/', views.material_detail, name='material_detail'),
    path('materials/<int:pk>/edit/', views.material_edit, name='material_edit'),
    
    # Process URLs
    path('processes/', views.process_list, name='process_list'),
    path('processes/create/', views.process_create, name='process_create'),
    path('processes/<int:pk>/', views.process_detail, name='process_detail'),
    path('processes/<int:pk>/edit/', views.process_edit, name='process_edit'),
    
    # Project URLs
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    
    # Building URLs
    path('project/<int:project_id>/buildings/', views.building_list, name='building_list'),
    path('project/<int:project_id>/buildings/create/', views.building_create, name='building_create'),
    path('building/<int:building_id>/edit/', views.building_edit, name='building_edit'),
    path('building/<int:building_id>/delete/', views.building_delete, name='building_delete'),
    
    # API URLs
    path('api/buildings-by-project/<int:project_id>/', views.get_buildings_by_project, name='buildings_by_project'),
    
    # Production URLs
    path('production/', views.production_list, name='production_list'),
    path('production/dashboard/', views.production_dashboard, name='production_dashboard'),
    path('production/create/', views.production_log_create, name='production_log_create'),
    path('production/<int:pk>/', views.production_log_detail, name='production_detail'),
    path('production/<int:pk>/edit/', views.production_log_edit, name='production_log_edit'),
    path('production/<int:pk>/delete/', views.production_log_delete, name='production_log_delete'),
    path('production/delete-selected/', views.production_log_bulk_delete, name='production_log_bulk_delete'),
    
    # Quality URLs
    path('quality/', views.quality_list, name='quality_list'),
    path('quality/create/<int:production_log_id>/', views.quality_check_create, name='quality_check_create'),
    
    # Material Usage URLs
    path('material-usage/create/<int:production_log_id>/', views.material_usage_create, name='material_usage_create'),
    
    # Raw Data URLs
    path('raw-data/', views.raw_data_list, name='raw_data_list'),
    path('raw-data/create/', views.raw_data_create, name='raw_data_create'),
    path('raw-data/<int:pk>/', views.raw_data_detail, name='raw_data_detail'),
    path('raw-data/<int:pk>/edit/', views.raw_data_edit, name='raw_data_edit'),
    path('raw-data/upload/', views.raw_data_upload, name='raw_data_upload'),
    
    # Filtered Log Designations URL
    path('get-filtered-log-designations/', views.get_filtered_log_designations, name='get_filtered_log_designations'),
    
    # Password Reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='core/password_reset.html',
             email_template_name='core/password_reset_email.html',
             subject_template_name='core/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='core/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='core/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='core/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
