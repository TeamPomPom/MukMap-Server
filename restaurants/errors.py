from core.errors import ErrorCollection, ResponseCode


class RestaurantAPIError(object):
    SEARCH_RESTAURANT_EMPTY_GEO_INFO = ErrorCollection(
        error_code="SEARCH_RESTAURANT_EMPTY_GEO_INFO",
        status=ResponseCode.INVALID_PARAMETER,
        message="You must send lat and lng data.",
    )

    SEARCH_RESTAURANT_EMPTY_QUERY_INFO = ErrorCollection(
        error_code="SEARCH_RESTAURANT_EMPTY_QUERY_INFO",
        status=ResponseCode.INVALID_PARAMETER,
        message="You must send query data.",
    )

    SEARCH_RESTAURANT_EMPTY_DEVICE_INFO = ErrorCollection(
        error_code="SEARCH_RESTAURANT_EMPTY_DEVICE_INFO",
        status=ResponseCode.INVALID_PARAMETER,
        message="You must send proper device token data.",
    )