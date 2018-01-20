import string
import random

from flask import Flask, render_template, abort, request, redirect, url_for

import markdown2

from db import pages
import user
import auth

# Set value for your site
PAGE_NAME_SUFFIX = ' - my web site'
PASSWORD_FILE = '/path/to/your/password/file'

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = [random.choice(string.ascii_letters + string.digits) for i in range(4096)]

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

        return redirect(url_for('secret_login'))


@app.route('/secrets/top')
def secret_top():
    return render_template('secret/top.html')


@app.route('/secrets/pages/new', methods=['GET', 'POST'])
def secret_new():
    if request.method == 'GET':
        return render_template('secret/new_edit.html', url=url_for('secret_new'), id_='', title='', raw=False)
    else:
        page_title = request.form['title']
        page_type = request.form['type']
        page_id = request.form['id']
        page_content = request.form['content']

        pages.new(id_=page_id, title=page_title, type_=page_type, content=page_content)
        return redirect(url_for('secret_top'))


@app.route('/secrets/pages/edit', methods=['GET', 'POST'])
def secret_edit():
    pass


@app.route('/secrets/pages/remove', methods=['POST'])
def secret_remove():
    pass


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
def error_404_not_found():
    return render_template('error/404.html', title='404 Not Found' + PAGE_NAME_SUFFIX)


# Before request
@app.before_request
def before_request():
    if request.path.startswith('/secrets') and not auth.check():
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
    app.run()
