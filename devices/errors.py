from core.errors import ErrorCollection, ResponseCode


class DeviceAPIError(object):
    CREATE_DEVICE_EMPTY_DEVICE_TOKEN = ErrorCollection(
        error_code="CREATE_DEVICE_EMPTY_DEVICE_TOKEN",
        status=ResponseCode.INVALID_PARAMETER,
        message="Need device token",
    )

    WRITE_CLICK_DEVICE_LOG_EMPTY_VIDEO_INFO = ErrorCollection(
        error_code="WRITE_CLICK_DEVICE_LOG_EMPTY_VIDEO_INFO",
        status=ResponseCode.INVALID_PARAMETER,
        message="You must send proper video data.",
    )