# Heroku buildpack: Sphinx

This is a [Heroku buildpack](http://devcenter.heroku.com/articles/buildpacks) for Sphinx documentation.


Usage
-----

Example usage:

    $ ls
    index.rst conf.py

    $ heroku create --buildpack git://github.com/Jc2k/heroku-buildpack-sphinx.git

    $ git push heroku master
    ...
    -----> Python app detected
    -----> Installing runtime (python-2.7.10)
    -----> Installing dependencies using pip
           Downloading/unpacking requests (from -r requirements.txt (line 1))
           Installing collected packages: requests
           Successfully installed requests
           Cleaning up...
    -----> Discovering process types
           Procfile declares types -> (none)

You can also add it to upcoming builds of an existing application:

    $ heroku buildpacks:set git://github.com/Jc2k/heroku-buildpack-sphinx.git
