#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import base64
from datetime import datetime, timezone

STRETCH_COUNT = 100000


def __add_salt(src: str, salt: [str]) -> str:
    results = []

    salt_len = len(salt)
    for i in range(16):
        results.append(src)
        results.append(salt[i % salt_len])

    return ''.join(results)


def compute_hash(src: str) -> str:
    salt = [
        base64.b16encode(src),
        base64.b32encode(src),
        base64.b64encode(src)
    ]

    for i in range(STRETCH_COUNT):
        src = hashlib.sha512(__add_salt(src, salt))

    return src


def get_current_datetime():
    return datetime.now(tz=timezone.utc)


def get_datetime_with_timezone(time_string, format_string, tz):
    dt = datetime.strptime(time_string, format_string)
    dt_tz = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, tz)
    return dt_tz
