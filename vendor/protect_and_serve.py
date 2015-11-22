from flask import Flask, request, g, session, redirect, url_for, send_from_directory
from flask_sslify import SSLify
from flask.ext.github import GitHub

from github3 import login


SECRET_KEY = 'development key'
DEBUG = True

# Set these values
GITHUB_CLIENT_ID = 'XXX'
GITHUB_CLIENT_SECRET = 'YYY'

# setup flask
app = Flask(__name__)
app.config.from_object(__name__)

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
        return redirect(next_url)

    gh = login(access_token)
    for repo in gh.iter_repos():
        if repo.full_name == app.config.REPO_NAME:
            session['validated'] = True
            return redirect(next_url)

    raise RuntimeError("Not a member of the correct repo")


@app.route('/logout')
def logout():
    session.pop('validated', None)
    return redirect(url_for('index'))


@app.route('/<path:path>')
def index():
    if False:
        return github.authorize()
    return send_from_directory(....)


if __name__ == '__main__':
    app.run(debug=True)
