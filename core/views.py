from django.http import JsonResponse
from django.conf import settings
import redis
import requests


def healthz(request):
    """Production health check endpoint"""
    checks = {}

    # Django healthy
    checks['django'] = 'healthy'

    # OMDb API healthy
    try:
        response = requests.get(f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t=test", timeout=3)
        checks['omdb'] = 'healthy' if response.status_code == 200 else 'unhealthy'
    except:
        checks['omdb'] = 'unhealthy'

    # All healthy?
    status = 'healthy' if all(v == 'healthy' for v in checks.values()) else 'unhealthy'

    return JsonResponse({
        'status': status,
        'checks': checks,
        'timestamp': '2026-03-05T12:00:00Z'
    })
