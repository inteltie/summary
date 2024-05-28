from rest_framework.permissions import BasePermission
from summary2.settings import X_API_KEY, CLIENT_SECRET

class ApiKeyPermission(BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get('x-api-key')
        client_secret = request.headers.get('client-secret')
        return api_key == X_API_KEY and client_secret in CLIENT_SECRET