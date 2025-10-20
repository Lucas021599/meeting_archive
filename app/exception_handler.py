from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.views import exception_handler, exceptions


def custom_exception_handler(exc, context):
    """
    모든 response에 code 추가하는 함수, 직접 사용하지 않고 setting에 추가하여 자동으로 불러지게 사용
    같은 status_code라도 구분 지을수 있는 code full detail 반환
    해당 code는 APIException으로 raise해야만 사용가능
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()
    response = exception_handler(exc, context)
    if isinstance(exc, exceptions.APIException):
        response.data = exc.get_full_details()
        if isinstance(exc, exceptions.ValidationError):
            response.data = {
                "message": "Invalid Parameter",
                "code": "invalid_parameter",
                "detail": response.data,
            }
        response.data["status_code"] = response.status_code
    return response
