################################################################################
# filename: urls.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 13/08,2025
################################################################################

from django.urls import include, path
from django.contrib import admin
from django.urls import path
from .view import csrf_token
from .view_wp import register_user, get_users

################################################################################

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('csrf/',csrf_token),
    path('register/',register_user),
    path('users/', get_users)
]

################################################################################
# End of File
################################################################################