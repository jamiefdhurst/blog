import os
import requests
from flask import Flask, g, render_template, url_for
from werkzeug.exceptions import HTTPException

def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.before_request
    def load_version():
        # pylint: disable=assigning-non-slot
        g.version = app.config['VERSION']

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    @app.errorhandler(Exception)
    def handle_exception(err):
        if isinstance(err, HTTPException):
            return err

        return render_template('500.html', err=err), 500

    @app.errorhandler(404)
    def page_not_found(err):
        return render_template('404.html', err=err), 404

    return app
