import six
from rest_framework import status, response
from rest_framework.exceptions import APIException


class ValidationError(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, detail, status):
        """

        :param detail: details of error
        :param status: status code
        """
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]
        self.detail = detail
        self.status_code = status

    def __str__(self):
        return six.text_type(self.detail)


class CustomResponse(object):
    def __init__(self, has_error=False, code=status.HTTP_200_OK, message="", data=None):
        self.has_error = has_error
        self.data = data
        self.code = code
        self.message = message

    def _get_data(self):
        data = dict(
            status=not self.has_error,
            code=self.code,
            message=self.message
        )
        if self.data is not None:
            data.update({'data': self.data})
        return data

    def response(self):
        return response.Response(self._get_data(), status=status.HTTP_200_OK)

    def error(self):
        self.has_error = True
        return ValidationError(self._get_data(), status=status.HTTP_200_OK)
