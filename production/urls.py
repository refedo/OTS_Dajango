from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('orders/', views.ProductionOrderListView.as_view(), name='order_list'),
    path('work-centers/', views.WorkCenterListView.as_view(), name='work_center_list'),
    path('schedule/', views.ProductionScheduleView.as_view(), name='schedule'),
    path('quality/', views.QualityControlListView.as_view(), name='quality_list'),
    path('reports/', views.ProductionReportListView.as_view(), name='report_list'),
    path('logging/', views.ProductionLoggingView.as_view(), name='logging'),
    path('list/', views.ProductionListView.as_view(), name='list'),
    path('create/', views.ProductionLogCreateView.as_view(), name='production_log_create'),
]
