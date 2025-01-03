from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.

class QualityControlListView(LoginRequiredMixin, ListView):
    template_name = 'quality/control_list.html'
    context_object_name = 'quality_controls'
    
    def get_queryset(self):
        # Placeholder until we create the models
        return []

class InspectionListView(LoginRequiredMixin, ListView):
    template_name = 'quality/inspection_list.html'
    context_object_name = 'inspections'
    
    def get_queryset(self):
        # Placeholder until we create the models
        return []

class QualityReportListView(LoginRequiredMixin, ListView):
    template_name = 'quality/report_list.html'
    context_object_name = 'reports'
    
    def get_queryset(self):
        # Placeholder until we create the models
        return []

class QualityStandardListView(LoginRequiredMixin, ListView):
    template_name = 'quality/standard_list.html'
    context_object_name = 'standards'
    
    def get_queryset(self):
        # Placeholder until we create the models
        return []
