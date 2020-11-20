from core.errors import ErrorCollection, ResponseCode


class DeviceAPIError(object):
    CREATE_DEVICE_EMPTY_DEVICE_TOKEN = ErrorCollection(
        error_code="CREATE_DEVICE_EMPTY_DEVICE_TOKEN",
        status=ResponseCode.INVALID_PARAMETER,
        message="Need device token",
    )