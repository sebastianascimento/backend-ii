"""
Views for the hello app.
"""
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@require_GET
def index(request):
    """
    Render the index page with a Hello World message.
    """
    logger.info("Index page accessed")
    return render(request, 'hello/index.html', {
        'message': 'Hello World from Django!',
    })

@csrf_exempt
@require_GET
def hello_api(request):
    """
    JSON API endpoint returning a Hello World message.
    """
    logger.info("API endpoint accessed")
    return JsonResponse({
        'message': 'Hello World from Django API!',
        'status': 'success',
    })