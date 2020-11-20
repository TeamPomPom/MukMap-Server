from core.errors import ErrorCollection, ResponseCode


class VideoAPIError(object):
    CREATE_VIDEO_INVALID_SUB_CATEGORY = ErrorCollection(
        error_code="CREATE_VIDEO_INVALID_SUB_CATEGORY",
        status=ResponseCode.INVALID_PARAMETER,
        message="Please give proper sub category pk, please check sub category data.",
    )

    CREATE_VIDEO_NEED_MORE_INFORMATION = ErrorCollection(
        error_code="CREATE_VIDEO_NEED_MORE_INFORMATION",
        status=ResponseCode.INVALID_PARAMETER,
        message="Need more information to create video info.",
    )

    CREATE_VIDEO_EMPTY_USER_ERROR = ErrorCollection(
        error_code="CREATE_VIDEO_EMPTY_USER_ERROR",
        status=ResponseCode.NEED_AUTH,
        message="Empty user error, please log in first.",
    )

    CREATE_VIDEO_INVALID_MAIN_CATEGORY = ErrorCollection(
        error_code="CREATE_VIDEO_INVALID_MAIN_CATEGORY",
        status=ResponseCode.INVALID_PARAMETER,
        message="Improper main food category id, please check main food data.",
    )

    CREATE_VIDEO_INVALID_CHANNEL = ErrorCollection(
        error_code="CREATE_VIDEO_INVALID_CHANNEL",
        status=ResponseCode.INVALID_PARAMETER,
        message="Improper channel id, please check channel data.",
    )

    CREATE_VIDEO_INVALID_RESTAURANT = ErrorCollection(
        error_code="CREATE_VIDEO_INVALID_RESTAURANT",
        status=ResponseCode.INVALID_PARAMETER,
        message="Improper restaurant id, please check restaurant data.",
    )

    GET_VIDEO_LIST_FORBIDDEN = ErrorCollection(
        error_code="GET_VIDEO_LIST_FORBIDDEN",
        status=ResponseCode.FORBIDDEN,
        message="Get entire list of video is forbidden.",
    )