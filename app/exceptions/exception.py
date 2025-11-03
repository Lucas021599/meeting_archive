from drf_spectacular.utils import OpenApiExample
from rest_framework import status
from rest_framework.exceptions import APIException


class CustomException(APIException):
    @classmethod
    def example(cls):
        return OpenApiExample(
            cls.default_detail,
            value={
                "message": cls.default_detail,
                "code": cls.default_code,
                "status_code": cls.status_code,
            },
            status_codes=[cls.status_code],
            response_only=True,
        )


class NotFoundException(CustomException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Not Found"
    default_code = "not_found"


class ParameterMissingException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Parameter Missing"
    default_code = "parameter_missing"


class InvalidParameterException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid Parameter"
    default_code = "invalid_parameter"
