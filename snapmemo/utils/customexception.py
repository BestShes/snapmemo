from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _

__all__ = (
    'AuthenticateException',
)


class AuthenticateException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Authentication credentials were not provided.')


class ValidationException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Validation Error')
