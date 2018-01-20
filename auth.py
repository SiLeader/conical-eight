#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import session
from datetime import timedelta, timezone
import utility as util

ID = 'id'
LIMIT = 'limit'

_LIMIT = timedelta(days=1)
_STR_FORMAT = '%Y-%m-%d %H:%M:%S'


def login(user_id):
    session[ID] = user_id
    session[LIMIT] = (util.get_current_datetime() + _LIMIT).strftime(_STR_FORMAT)


def check():
    if session.get(ID) is None or session.get(LIMIT) is None:
        logout()
        return False

    dt = util.get_datetime_with_timezone(session[LIMIT], _STR_FORMAT, timezone.utc)
    current = util.get_current_datetime()

    if dt <= current:
        logout()
        return False

    login(session[ID])
    return True


def logout():
    if session.get(ID) is not None:
        session.pop(ID)
    if session.get(LIMIT) is not None:
        session.pop(LIMIT)


def get_id():
    if check():
        return session[ID]
    return None
