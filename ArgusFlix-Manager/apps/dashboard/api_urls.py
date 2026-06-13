from django.urls import path
from .views import dashboard_view, settings_view, live_dashboard_data, visual_stats_data

app_name = 'dashboard'

urlpatterns = [
    path('dashboard-data/', live_dashboard_data, name='dashboard_data'),
    path('visual-stats/', visual_stats_data, name='visual_stats'),
]
