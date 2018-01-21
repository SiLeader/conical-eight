#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   Copyright 2018 SiLeader.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import hashlib
import base64
from datetime import datetime, timezone

STRETCH_COUNT = 100000


def __add_salt(src: str, salt: [str]):
    results = []

    salt_len = len(salt)
    for i in range(16):
        results.append(src)
        results.append(salt[i % salt_len])

    return ''.join(results)


def compute_hash(src: str) -> str:
    salt = [
        base64.b16encode(src.encode('utf-8')).decode('utf-8'),
        base64.b32encode(src.encode('utf-8')).decode('utf-8'),
        base64.b64encode(src.encode('utf-8')).decode('utf-8')
    ]

    for i in range(STRETCH_COUNT):
        src = hashlib.sha512(__add_salt(src, salt).encode('utf-8')).hexdigest()

    return src


def get_current_datetime():
    return datetime.now(tz=timezone.utc)


def get_datetime_with_timezone(time_string, format_string, tz):
    dt = datetime.strptime(time_string, format_string)
    dt_tz = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, tz)
    return dt_tz
