from core.errors import ErrorCollection, ResponseCode


class ApplicationConfigAPIError(object):
    APPLICATION_EMPTY_PARAMETER = ErrorCollection(
        error_code="APPLICATION_EMPTY_PARAMETER",
        status=ResponseCode.INVALID_PARAMETER,
        message="You must send all required data.",
    )

    INVALID_PLATFORM_NAME = ErrorCollection(
        error_code="INVALID_PLATFORM_NAME",
        status=ResponseCode.INVALID_PARAMETER,
        message="You must send valid platform name.",
    )

    INVALID_APP_NAME = ErrorCollection(
        error_code="INVALID_APP_NAME",
        status=ResponseCode.INVALID_PARAMETER,
        message="You must send valid app name.",
    )