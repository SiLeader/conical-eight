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
__col = __db.pages

ID = 'id'
TITLE = 'title'
TYPE = 'type'
CONTENT = 'content'

TYPE_MARKDOWN = 'markdown'
# TYPE_ASCIIDOC = 'asciidoc'
TYPE_RAW = 'raw'


"""
id: str      -> unique -> page id. example.com/<id>
title: str   ->        -> page title.
type: str    ->        -> page type. Markdown or RAW
content: str ->        -> page content. written in <type>.
"""


def new(id_: str, title: str, type_: str, content: str) -> bool:
    """
    add new page
    :param id_: page id
    :param title: page title
    :param type_: page type
    :param content: page content
    :return: true -> success, false -> ID already exist
    """
    if exists(id_):
        return False

    __col.insert({
        ID: id_,
        TITLE: title,
        TYPE: type_,
        CONTENT: content
    })
    return True


def exists(id_: str) -> bool:
    """
    check existence of ID
    :param id_: page id
    :return: true -> exist, false -> not exist
    """
    return __col.find({ID: id_}).count() > 0


def get(id_: str) -> dict:
    """
    get page by ID
    :param id_: page id
    :return: None -> Not found, dict -> page information
    """
    return __col.find_one({ID: id_})


def update(id_: str, title: str=None, type_: str=None, content: str=None) -> bool:
    """
    update page
    :param id_: target page id
    :param title: page title (Optional)
    :param type_: page type (Optional)
    :param content: page content (Optional)
    :return: true -> success, false -> error caused
    """
    doc = {}
    if title is not None:
        doc[TITLE] = title
    if type_ is not None:
        doc[TYPE] = type_
    if content is not None:
        doc[CONTENT] = content
    return __col.update_one({ID: id_}, {'$set': doc}).acknowledged


def remove(id_: str) -> bool:
    """
    remove page
    :param id_: target page id
    :return: true -> success, false -> error caused
    """
    return __col.delete_one({ID: id_}).acknowledged


def get_list():
    """
    get questions list
    :return: questions list
    """
    return list(__col.find())
