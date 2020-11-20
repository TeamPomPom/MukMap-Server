from core.errors import ErrorCollection, ResponseCode


class ChannelAPIError(object):
    CREATE_CHANNEL_ALREADY_REGISTERED = ErrorCollection(
        error_code="CREATE_CHANNEL_ALREADY_REGISTERED",
        status=ResponseCode.ALREADY_PROCESSED,
        message="Sign up process already registered",
    )

    GET_CHANNEL_DETAIL_INVALID_TOP_N_VARIABLE = ErrorCollection(
        error_code="GET_CHANNEL_DETAIL_INVALID_TOP_N_VARIABLE",
        status=ResponseCode.INVALID_PARAMETER,
        message="top_n must be natural number",
    )