################################################################################
# filename: urls.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 13/08,2025
################################################################################

from django.urls import include, path
from django.contrib import admin
from django.urls import path

################################################################################

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
]

################################################################################
# End of File
################################################################################