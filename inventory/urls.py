from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('materials/', views.MaterialListView.as_view(), name='material_list'),
    path('materials/<str:type>/<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),
    path('materials/<str:type>/add/', views.MaterialCreateView.as_view(), name='material_create'),
    path('materials/<str:type>/<int:pk>/edit/', views.MaterialUpdateView.as_view(), name='material_update'),
]
