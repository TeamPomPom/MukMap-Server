from core.errors import ErrorCollection, ResponseCode


class UserAPIError(object):
    USER_INFO_EMPTY_USER_NAME = ErrorCollection(
        error_code="USER_INFO_EMPTY_USER_NAME",
        status=ResponseCode.INVALID_PARAMETER,
        message="You must send user name.",
    )

    FAILED_TO_LOGIN = ErrorCollection(
        error_code="FAILED_TO_LOGIN",
        status=ResponseCode.UNAUTHORIZED,
        message="Failed to login, please check login params.",
    )

    USER_INFO_EMPTY_SNS_ID = ErrorCollection(
        error_code="USER_INFO_EMPTY_SNS_ID",
        status=ResponseCode.INVALID_PARAMETER,
        message="You must send SNS id properly.",
    )
    CREATE_USER_DUPLICATE_USER = ErrorCollection(
        error_code="CREATE_USER_DUPLICATE_USER",
        status=ResponseCode.DUPLICATE_PROPERTY,
        message="User already exist.",
    )
