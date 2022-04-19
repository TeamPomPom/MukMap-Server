from core.errors import ErrorCollection, ResponseCode


class DeviceAPIError(object):
    NEED_TO_CREATE_DEVICE_RECORD = ErrorCollection(
        error_code="NEED_TO_CREATE_DEVICE_RECORD",
        status=ResponseCode.NOT_FOUND,
        message="Need to create device record in DB"
    )

    ALREADY_REGISTERED_DEVICE = ErrorCollection(
        error_code="ALREADY_REGISTERED_DEVICE",
        status=ResponseCode.ALREADY_PROCESSED,
        message="Already device id is recorded in DB"
    )

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
    DEVICE_FAVORITE_INVALID_RESTAURANT = ErrorCollection(
        error_code="DEVICE_FAVORITE_INVALID_RESTAURANT",
        status=ResponseCode.INVALID_PARAMETER,
        message="Improper restaurant id, please check restaurant data.",
    )
    DEVICE_SUBSCRIBE_INVALID_CHANNEL = ErrorCollection(
        error_code="DEVICE_SUBSCRIBE_INVALID_CHANNEL",
        status=ResponseCode.INVALID_PARAMETER,
        message="Improper channel id, please check channel data.",
    )