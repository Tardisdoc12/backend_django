################################################################################
# filename: urls.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 13/08,2025
################################################################################

from django.urls import path
from . import views

################################################################################

urlpatterns = [
    path('', views.list_events, name='event_list'),
    path('create/', views.create_event, name='event_create'),
    path('delete/<int:pk>', views.delete_event, name='event_delete'),
    path('inscrit/<int:event_id>', views.get_list_inscript, name="event_inscrit_list"),
    path('inscrit/create/', views.create_inscrit, name="inscription_user"),
    path('update/<int:event_id>/', views.update_event, name='event_update'),
]

################################################################################
# End of File
################################################################################