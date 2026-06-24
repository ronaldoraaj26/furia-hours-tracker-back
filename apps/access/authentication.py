from rest_framework import authentication, exceptions

from .models import Token


class AccessTokenAuthentication(authentication.BaseAuthentication):
    keyword = 'Token'

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).decode('utf-8')
        if not auth_header:
            return None
        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            return None
        raw_token = parts[1]
        try:
            access_token = Token.objects.select_related('user').get(token=raw_token)
        except Token.DoesNotExist as exc:
            raise exceptions.AuthenticationFailed('Token inválido.') from exc
        if not access_token.is_valid:
            raise exceptions.AuthenticationFailed('Token expirado ou revogado.')
        return access_token.user, access_token
