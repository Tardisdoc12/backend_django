################################################################################
# filename: view.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 16/08,2025
################################################################################

from django.middleware.csrf import get_token
from django.http import JsonResponse

################################################################################

def csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})

################################################################################
# End of File
################################################################################