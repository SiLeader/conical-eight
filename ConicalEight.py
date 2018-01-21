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

from flask import Flask, render_template, abort, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect

import markdown2

from db import pages
import user
import auth

from settings import PAGE_NAME_SUFFIX

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(4096)])
csrf = CSRFProtect(app)

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
    return render_template('secret/top.html', pages=pages_)


@app.route('/secrets/pages/new', methods=['GET', 'POST'])
def secret_new():
    if request.method == 'GET':
        return render_template('secret/new_edit.html',
                               url=url_for('secret_new'),
                               id_='',
                               title='',
                               raw=False,
                               content='')
    else:
        page_title = request.form['title']
        page_type = request.form['type']
        page_id = request.form['id']
        page_content = request.form['content']

        pages.new(id_=page_id, title=page_title, type_=page_type, content=page_content)
        return redirect(url_for('secret_top'))


@app.route('/secrets/pages/edit/<page_id>', methods=['GET', 'POST'])
def secret_edit(page_id):
    if request.method == 'GET':
        page = pages.get(page_id)
        return render_template('secret/new_edit.html',
                               url=url_for('secret_edit', page_id=page_id),
                               id_=page[pages.ID],
                               title=page[pages.TITLE],
                               raw=(page[pages.TYPE] == pages.TYPE_RAW),
                               content=page[pages.CONTENT])
    else:
        page_title = request.form['title']
        page_type = request.form['type']
        page_id = request.form['id']
        page_content = request.form['content']

        pages.update(id_=page_id, title=page_title, type_=page_type, content=page_content)
        return redirect(url_for('secret_top'))


@app.route('/secrets/pages/remove/<page_id>')
def secret_remove(page_id):
    pages.remove(page_id)
    return redirect(url_for('secret_top'))


# Utility
def render_page(page_id: str):
    page = pages.get(page_id)
    if page is None:
        abort(404)

    page_content = page[pages.CONTENT]

    page_type = page[pages.TYPE]
    if page_type == pages.TYPE_MARKDOWN:
        page_content = markdown2.markdown(page_content)

    return render_template('content/page.html', title=page[pages.TITLE] + PAGE_NAME_SUFFIX, content=page_content)


# Error Handlers
@app.errorhandler(404)
def error_404_not_found(err):
    return render_template('error/404.html', title='404 Not Found' + PAGE_NAME_SUFFIX), err.code


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
