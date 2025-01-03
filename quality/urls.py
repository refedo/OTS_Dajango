from django.urls import path
from . import views

app_name = 'quality'

urlpatterns = [
    path('control/', views.QualityControlListView.as_view(), name='control_list'),
    path('inspections/', views.InspectionListView.as_view(), name='inspections'),
    path('reports/', views.QualityReportListView.as_view(), name='reports'),
    path('standards/', views.QualityStandardListView.as_view(), name='standards'),
]
