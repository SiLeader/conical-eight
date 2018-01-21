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

import os

from settings import PASSWORD_FILE
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
            line = fp.readline().rstrip('\n')
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
    if not os.path.exists(PASSWORD_FILE):
        return False
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
