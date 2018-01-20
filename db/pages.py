#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo
from typing import Optional


__client = pymongo.MongoClient()
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
    return __col.conut({ID: id_}) <= 0


def get(id_: str) -> Optional[dict]:
    """
    get page by ID
    :param id_: page id
    :return: None -> Not found, dict -> page information
    """
    return __col.find_one({ID: id_})


def update(id_: str, title: Optional[str]=None, type_: Optional[str]=None, content: Optional[str]=None) -> bool:
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
