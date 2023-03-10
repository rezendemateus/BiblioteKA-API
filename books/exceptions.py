from rest_framework.exceptions import APIException, status


class ConflitcError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "This book has already been added."
    default_code = "parse_error"
