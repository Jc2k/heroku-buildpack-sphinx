import os
from flask import Flask, abort, request, g, session, redirect, url_for, send_from_directory
from flask_sslify import SSLify
from flask.ext.github import GitHub

from github3 import login


# setup flask
app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "development key"),
    GITHUB_CLIENT_ID=os.environ.get("GITHUB_CLIENT_ID", "xx"),
    GITHUB_CLIENT_SECRET=os.environ.get("GITHUB_CLIENT_ID", "yy"),
    STATIC_DIR=os.environ.get("STATIC_DIR", "."),
    DEBUG=True,
)

# Enforce use of SSL
sslify = SSLify(app)

# GitHub backed authentication
github = GitHub(app)


@github.access_token_getter
def token_getter():
    return session.get('github_access_token')


@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    if access_token is None:
        return abort(403)

    gh = login(access_token)
    for repo in gh.iter_repos():
        if repo.full_name == app.config.REPO_NAME:
            session['validated'] = True
            return redirect(next_url)

    return abort(403)


@app.route('/logout')
def logout():
    session.pop('validated', None)
    return redirect(url_for('index'))


@app.route('/')
def index():
    return redirect('/index.html')


@app.route('/<path:filename>')
def path(filename):
    if session.get('validated', False):
        return github.authorize(scope="user,repo")
    return send_from_directory(
        app.config.STATIC_DIR,
        filename,
    )


if __name__ == '__main__':
    app.run(debug=True)
