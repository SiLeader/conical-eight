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

import pymongo


__client = pymongo.MongoClient('localhost')
__db = __client.conical_eight
__col = __db.tags

ID = 'id'
NAME = 'name'

"""
id: str      -> unique, immutable -> tag id.
name: str    -> unique            -> tag name.
"""


def new(id_: str, name: str) -> bool:
    """
    add new tag
    :param id_: tag id
    :param name: tag name
    :return: true -> success, false -> ID already exist
    """
    if exists(id_=id_, name=name):
        return False

    __col.insert({
        ID: id_,
        NAME: name
    })
    return True


def exists(id_: str=None, name: str=None) -> bool:
    """
    check existence of ID
    :param id_: tag id
    :param name: tag name
    :return: true -> exist, false -> not exist
    """
    query = {}
    if id_ is None and name is None:
        return False

    if id_ is not None:
        query[ID] = id_
    if name is not None:
        query[NAME] = name

    return __col.find(query).count() > 0


def get(id_: str) -> dict:
    """
    get tag by ID
    :param id_: tag id
    :return: None -> Not found, dict -> tag information
    """
    return __col.find_one({ID: id_})


def update(id_: str, name: str=None) -> bool:
    """
    update tag
    :param id_: target tag id
    :param name: tag name
    :return: true -> success, false -> error caused
    """
    doc = {}
    if name is None or exists(name=name):
        return False
    doc[NAME] = name

    return __col.update_one({ID: id_}, {'$set': doc}).acknowledged


def remove(id_: str) -> bool:
    """
    remove tag
    :param id_: target tag id
    :return: true -> success, false -> error caused
    """
    return __col.delete_one({ID: id_}).acknowledged


def get_list():
    """
    get questions list
    :return: questions list
    """
    return list(__col.find())
