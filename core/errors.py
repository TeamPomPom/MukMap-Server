class ErrorCollection(object):
    def __init__(self, error_code, status, message):
        self.error_code = error_code
        self.status = status
        self.message = message

    def __str__(self):
        error_msg = {}
        error_msg["error_code"] = self.error_code
        error_msg["status"] = self.status
        error_msg["message"] = self.message
        return str(error_msg)


class ResponseCode(object):
    RESPONSE_OK = 1
    NOT_FOUND = 2
    INVALID_PARAMETER = 3
    NEED_AUTH = 4
    DUPLICATE_PROPERTY = 5
    ALREADY_PROCESSED = 6
    FORBIDDEN = 7
    UNAUTHORIZED = 8
