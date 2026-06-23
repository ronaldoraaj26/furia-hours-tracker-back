import json

from django.utils.deprecation import MiddlewareMixin

from .models import AuditLog


class AuditLogMiddleware(MiddlewareMixin):
    MUTATING_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}

    def process_response(self, request, response):
        if request.path.startswith('/api/') and request.method in self.MUTATING_METHODS and response.status_code < 500:
            user = request.user if getattr(request, 'user', None) and request.user.is_authenticated else None
            payload = {}
            if request.content_type == 'application/json':
                try:
                    payload = json.loads(request.body.decode('utf-8') or '{}')
                except Exception:
                    payload = {}
            AuditLog.objects.create(
                user=user,
                action=request.method,
                entity=request.path,
                details=json.dumps({
                    'status_code': response.status_code,
                    'payload': payload,
                }, ensure_ascii=False),
            )
        return response
