from collections import Counter


def meok_to_bool(value):
    """
    Converts 'something' to boolean. Raises exception for invalid formats
        Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
        Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if str(value).lower() in ("yes", "y", "true", "t", "1"):
        return True
    if str(value).lower() in (
        "no",
        "n",
        "false",
        "f",
        "0",
        "0.0",
        "",
        "none",
        "[]",
        "{}",
    ):
        return False
    raise Exception("Invalid value for boolean conversion: " + str(value))


def common_list(value_list, n_th):
    c = Counter(value_list)
    return c.most_common(n_th)