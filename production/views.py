from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ProductionLog

# Create your views here.

class ProductionOrderListView(LoginRequiredMixin, ListView):
    template_name = 'production/order_list.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        # Placeholder until we create the models
        return []

class WorkCenterListView(LoginRequiredMixin, ListView):
    template_name = 'production/work_center_list.html'
    context_object_name = 'work_centers'
    
    def get_queryset(self):
        # Placeholder until we create the models
        return []

class ProductionScheduleView(LoginRequiredMixin, ListView):
    template_name = 'production/schedule.html'
    context_object_name = 'schedule_items'
    
    def get_queryset(self):
        # Placeholder until we create the models
        return []

class QualityControlListView(LoginRequiredMixin, ListView):
    template_name = 'production/quality_list.html'
    context_object_name = 'quality_items'
    
    def get_queryset(self):
        # Placeholder until we create the models
        return []

class ProductionReportListView(LoginRequiredMixin, ListView):
    template_name = 'production/report_list.html'
    context_object_name = 'reports'
    
    def get_queryset(self):
        # Placeholder until we create the models
        return []

class ProductionLoggingView(LoginRequiredMixin, ListView):
    template_name = 'production/logging.html'
    context_object_name = 'logs'
    
    def get_queryset(self):
        # Placeholder until we create the models
        return []

class ProductionListView(LoginRequiredMixin, ListView):
    template_name = 'production/list.html'
    context_object_name = 'productions'
    
    def get_queryset(self):
        # Placeholder until we create the models
        return []

class ProductionLogCreateView(LoginRequiredMixin, CreateView):
    model = ProductionLog
    template_name = 'production/production_log_form.html'
    fields = ['name', 'description', 'status', 'start_date', 'end_date', 'notes']
    success_url = reverse_lazy('production:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
