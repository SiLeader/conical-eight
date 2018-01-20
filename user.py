#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ConicalEight import PASSWORD_FILE
from utility import compute_hash
from getpass import getpass


def __add_user(name: str, password: str) -> bool:
    if __exists(name):
        return False
    with open(PASSWORD_FILE, 'a') as fp:
        fp.write('{0}:{1}\n'.format(name, compute_hash(password)))
    return True


def check(name: str, password: str):
    with open(PASSWORD_FILE) as fp:
        while True:
            line = fp.readline()
            if not line:
                break

            if ':' not in line:
                continue

            up = line.split(':')
            if up[0] == name:
                if up[1] == compute_hash(password):
                    return True
                break
    return False


def __exists(name: str) -> bool:
    with open(PASSWORD_FILE) as fp:
        while True:
            line = fp.readline()
            if not line:
                break

            if ':' not in line:
                continue

            up = line.split(':')
            if up[0] == name:
                return True
    return False


if __name__ == '__main__':
    name_ = input('User ID: ')
    password_ = getpass()

    if __add_user(name_, password_):
        print('Add new user successfully')
    else:
        print('Failed to add user')
        exit(1)
