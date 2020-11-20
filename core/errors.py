class ErrorCollection(object):
    def __init__(self, error_code, status, message):
        self.error_code = error_code
        self.status = status
        self.message = message

    def as_json_object(self):
        return '{"error_code": "%s", "status_code": "%s", "message": "%s"}' % (
            self.error_code,
            self.status,
            self.message,
        )


class ResponseCode(object):
    RESPONSE_OK = 1
    NOT_FOUND = 2
    INVALID_PARAMETER = 3
