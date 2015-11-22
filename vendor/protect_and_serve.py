import os
import logging

from flask import Flask, abort, request, g, session, redirect, url_for, send_from_directory
from flask_sslify import SSLify
from flask.ext.github import GitHub

from github3 import login


# setup flask
app = Flask(__name__)
app.config.update(
    PREFERRED_URL_SCHEME='https',
    SECRET_KEY=os.environ.get("SECRET_KEY", "development key"),
    GITHUB_CLIENT_ID=os.environ.get("GITHUB_CLIENT_ID", "xx"),
    GITHUB_CLIENT_SECRET=os.environ.get("GITHUB_CLIENT_SECRET", "yy"),
    STATIC_DIR=os.environ.get("STATIC_DIR", "."),
    REPO_NAME=os.environ.get("REPO_NAME", "!"),
)

# Enforce use of SSL
sslify = SSLify(app)

# GitHub backed authentication
github = GitHub(app)


@app.before_first_request
def setup_logging():
    if not app.debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)


@github.access_token_getter
def token_getter():
    return session.get('github_access_token')


@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    if access_token is None:
        return abort(403)

    gh = login(token=access_token)
    app.logger.info("A")
    app.logger.info(app.config['REPO_NAME'])
    for repo in gh.iter_repos():
        app.logger.info(repo.full_name)
        if repo.full_name == app.config['REPO_NAME']:
            session['validated'] = True
            return redirect(next_url)
    app.logger.info("B")
    return abort(403)


@app.route('/logout')
def logout():
    session.pop('validated', None)
    return redirect(url_for('index'))


@app.route('/')
def index():
    return redirect(url_for('path', filename='index.html'))


@app.route('/<path:filename>')
def path(filename):
    if not session.get('validated', False):
        return github.authorize(scope="user,repo")
    return send_from_directory(
        app.config['STATIC_DIR'],
        filename,
    )


if __name__ == '__main__':
    app.run(debug=True)
