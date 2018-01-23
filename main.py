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

import string
import random
import os
import re

from flask import Flask, render_template, abort, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect

import markdown
from bs4 import BeautifulSoup

from db import pages, tags
import user
import auth

import settings

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(4096)])
csrf = CSRFProtect(app)

# Constants
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = FILE_DIR + '/static'

"""
Top page (example.com/)'s database page id: #top
"""


# Routing pages
@app.route('/')
def top_page():
    return render_page('#top')


@app.route('/<page_id>')
def some_pages(page_id):
    return render_page(page_id)


# Secret pages
@app.route('/secrets/login', methods=['GET', 'POST'])
def secret_login():
    if request.method == 'GET':
        return render_template('secret/login.html')
    else:
        user_id = request.form['user_id']
        password = request.form['password']
        if user.check(user_id, password):
            auth.login(user_id)
            return redirect(url_for('secret_top'))

        return redirect(url_for('secret_login'))


@app.route('/secrets/top')
def secret_top():
    pages_ = pages.get_list()
    files = [
        {'path': 'static/' + file, 'name': file}
        for file in os.listdir(RESOURCE_DIR) if os.path.isfile(RESOURCE_DIR + '/' + file)]

    return render_template('secret/top.html', pages=pages_, files=files, tags=tags.get_list())


@app.route('/secrets/pages/new', methods=['GET', 'POST'])
def secret_new():
    if request.method == 'GET':
        tags_ = tags.get_list()
        for tag in tags_:
            tag['exists'] = False
        return render_template('secret/new_edit.html',
                               url=url_for('secret_new'),
                               id_='',
                               title='',
                               raw=False,
                               content='',
                               tags=tags_)
    else:
        page_title = request.form['title']
        page_type = request.form['type']
        page_id = request.form['id']
        page_content = request.form['content'].replace('\r\n', '\n')
        page_tags = request.form.getlist('tags')

        if page_type == pages.TYPE_MARKDOWN:
            html = markdown.markdown(page_content, extensions=['gfm'], extras=['fenced-code-blocks'])
        else:
            html = page_content
        links = analyze_html(html)
        if '/' + page_id in links:
            links.remove('/' + page_id)

        pages.new(id_=page_id, title=page_title, type_=page_type, content=page_content, tags=page_tags, link_to=links)

        if settings.BACKUP_ENABLED:
            if settings.BACKUP_AS_HTML:
                backup_content = html
            else:
                backup_content = page_content
            path = settings.BACKUP_DIRECTORY_PATH + '/' + page_id
            if page_type == pages.TYPE_MARKDOWN:
                path += '.md'
            else:
                path += '.html'
            backup(backup_content, path)

        return redirect(url_for('secret_top'))


@app.route('/secrets/pages/edit/<page_id>', methods=['GET', 'POST'])
def secret_edit(page_id):
    if request.method == 'GET':
        page = pages.get(page_id)
        tags_ = tags.get_list()
        for tag in tags_:
            if pages.TAGS not in page or tag['id'] not in page[pages.TAGS]:
                tag['exists'] = False
            else:
                tag['exists'] = True
        return render_template('secret/new_edit.html',
                               url=url_for('secret_edit', page_id=page_id),
                               id_=page[pages.ID],
                               title=page[pages.TITLE],
                               raw=(page[pages.TYPE] == pages.TYPE_RAW),
                               content=page[pages.CONTENT],
                               tags=tags_)
    else:
        page_title = request.form['title']
        page_type = request.form['type']
        page_id = request.form['id']
        page_content = request.form['content'].replace('\r\n', '\n')
        page_tags = request.form.getlist('tags')

        if page_type == pages.TYPE_MARKDOWN:
            html = markdown.markdown(page_content, extensions=['gfm'], extras=['fenced-code-blocks'])
        else:
            html = page_content
        links = analyze_html(html)
        if '/' + page_id in links:
            links.remove('/' + page_id)

        pages.update(id_=page_id, title=page_title, type_=page_type, content=page_content, tags=page_tags)

        if settings.BACKUP_ENABLED:
            if settings.BACKUP_AS_HTML:
                backup_content = html
            else:
                backup_content = page_content
            path = settings.BACKUP_DIRECTORY_PATH + '/' + page_id
            if page_type == pages.TYPE_MARKDOWN:
                path += '.md'
            else:
                path += '.html'
            backup(backup_content, path)

        return redirect(url_for('secret_top'))


@app.route('/secrets/pages/remove/<page_id>')
def secret_remove(page_id):
    pages.remove(page_id)
    return redirect(url_for('secret_top'))


@app.route('/secrets/tags', methods=['POST'])
def secret_tag_post():
    id_ = request.form['id']
    name = request.form['name']
    if tags.exists(id_=id_):
        tags.update(id_, name)
    else:
        tags.new(id_, name)
    return redirect(url_for('secret_top'))


@app.route('/secrets/tags/remove/<tag_id>')
def secret_tag_remove(tag_id):
    tags.remove(tag_id)
    return redirect(url_for('secret_top'))


@app.route('/secrets/files', methods=['POST'])
def secret_file_post():
    if request.files.getlist('upload_files')[0].filename:
        upload_files = request.files.getlist('upload_files')
        for file in upload_files:
            file.save(RESOURCE_DIR + '/' + secure_filename(file.filename))
    return redirect(url_for('secret_top'))


@app.route('/secrets/files/remove/<file>')
def secret_file_remove(file):
    file = RESOURCE_DIR + '/' + file
    if os.path.exists(file):
        os.remove(file)
    return redirect(url_for('secret_top'))


# Utility
def render_page(page_id: str):
    page = pages.get(page_id)
    if page is None:
        abort(404)

    page_content = page[pages.CONTENT]

    page_type = page[pages.TYPE]
    if page_type == pages.TYPE_MARKDOWN:
        page_content = markdown.markdown(page_content, extensions=['gfm'], extras=['fenced-code-blocks'])

    page_content = process_related(page_content, pages.get_by_link(['/' + page_id]))

    return render_template('content/page.html',
                           title=page[pages.TITLE] + settings.PAGE_NAME_SUFFIX, content=page_content)


def process_related(html: str, linked_pages: [dict]):
    link = ['<ul>']
    for lp in linked_pages:
        link.append('<li><a href="/{0}">{1}</a></li>'.format(lp[pages.ID], lp[pages.TITLE]))
    link.append('</ul>')
    html = re.sub(r'(<\s*x-related\s*/>|<\s*x-related\s*>\s*</\s*x-related\s*>)', '\n'.join(link), html)

    return html


def analyze_html(html: str) -> [str]:
    soup = BeautifulSoup(html)
    links = []
    for a in soup.find_all('a'):
        href = a.get('href')
        if href.startswith('/'):
            if href == '/':
                href = '/#top'
            links.append(href)
    return links


def backup(data: str, path: str):
    with open(path, 'w') as fp:
        fp.write(data)


# Error Handlers
@app.errorhandler(404)
def error_404_not_found(err):
    return render_template('error/404.html', title='404 Not Found' + settings.PAGE_NAME_SUFFIX), err.code


# Before request
@app.before_request
def before_request():
    if request.path.startswith('/secrets') and not request.path == '/secrets/login' and not auth.check():
        return redirect("/")


# After request
@app.after_request
def apply_caching(res):
    res.headers['X-Frame-Options'] = 'SAMEORIGIN'
    res.headers['X-XSS-Protection'] = '1;mode=block'
    res.headers['X-Content-Type-Options'] = 'nosniff'
    res.headers['X-Powered-By'] = 'ConicalEight'
    return res


if __name__ == '__main__':
    app.run(debug=True)
