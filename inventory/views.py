from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import (
    BeamMaterial, SheetMaterial, AngleMaterial, PipeMaterial,
    TubeMaterial, PurlinMaterial, BarMaterial, FastenerMaterial,
    PanelMaterial, MiscMaterial
)

class MaterialListView(LoginRequiredMixin, ListView):
    template_name = 'inventory/material_list.html'
    context_object_name = 'materials'
    paginate_by = 20

    def get_queryset(self):
        material_type = self.request.GET.get('type', 'beam')
        search_query = self.request.GET.get('search', '')
        
        # Map URL parameters to model classes
        model_map = {
            'beam': BeamMaterial,
            'sheet': SheetMaterial,
            'angle': AngleMaterial,
            'pipe': PipeMaterial,
            'tube': TubeMaterial,
            'purlin': PurlinMaterial,
            'bar': BarMaterial,
            'fastener': FastenerMaterial,
            'panel': PanelMaterial,
            'misc': MiscMaterial,
        }
        
        model = model_map.get(material_type, BeamMaterial)
        queryset = model.objects.all()
        
        if search_query:
            queryset = queryset.filter(
                Q(code__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material_type'] = self.request.GET.get('type', 'beam')
        context['search_query'] = self.request.GET.get('search', '')
        return context

class MaterialDetailView(LoginRequiredMixin, DetailView):
    template_name = 'inventory/material_detail.html'
    context_object_name = 'material'

    def get_queryset(self):
        material_type = self.kwargs.get('type')
        model_map = {
            'beam': BeamMaterial,
            'sheet': SheetMaterial,
            'angle': AngleMaterial,
            'pipe': PipeMaterial,
            'tube': TubeMaterial,
            'purlin': PurlinMaterial,
            'bar': BarMaterial,
            'fastener': FastenerMaterial,
            'panel': PanelMaterial,
            'misc': MiscMaterial,
        }
        return model_map.get(material_type, BeamMaterial).objects.all()

class MaterialCreateView(LoginRequiredMixin, CreateView):
    template_name = 'inventory/material_form.html'
    
    def get_form_class(self):
        material_type = self.kwargs.get('type')
        model_map = {
            'beam': BeamMaterial,
            'sheet': SheetMaterial,
            'angle': AngleMaterial,
            'pipe': PipeMaterial,
            'tube': TubeMaterial,
            'purlin': PurlinMaterial,
            'bar': BarMaterial,
            'fastener': FastenerMaterial,
            'panel': PanelMaterial,
            'misc': MiscMaterial,
        }
        return model_map.get(material_type, BeamMaterial)

    def get_success_url(self):
        return reverse_lazy('material_list') + f'?type={self.kwargs.get("type")}'

class MaterialUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/material_form.html'
    
    def get_queryset(self):
        material_type = self.kwargs.get('type')
        model_map = {
            'beam': BeamMaterial,
            'sheet': SheetMaterial,
            'angle': AngleMaterial,
            'pipe': PipeMaterial,
            'tube': TubeMaterial,
            'purlin': PurlinMaterial,
            'bar': BarMaterial,
            'fastener': FastenerMaterial,
            'panel': PanelMaterial,
            'misc': MiscMaterial,
        }
        return model_map.get(material_type, BeamMaterial).objects.all()

    def get_success_url(self):
        return reverse_lazy('material_list') + f'?type={self.kwargs.get("type")}'
