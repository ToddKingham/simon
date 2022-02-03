from time import time as now


def has_expired(start, expiry):
    return now() > start + expiry
