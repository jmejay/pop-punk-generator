import os

from flask import Flask, session
from datetime import timedelta

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'jeem.sqlite'),
        PERMANENT_SESSION_LIFETIME=timedelta(days=7)

    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass





    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    app.add_url_rule('/', endpoint='login')

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/blog', endpoint='blog')

    from . import album
    app.register_blueprint(album.bp)
    app.add_url_rule('/album', endpoint='album')

    from . import history
    app.register_blueprint(history.bp)
    app.add_url_rule('/history', endpoint='history')

    from . import stats
    app.register_blueprint(stats.bp)
    app.add_url_rule('/stats', endpoint='history')

    return app

# Create the app instance
app = create_app()

# This ensures that when imported, it returns 'jeem:app'
if __name__ == '__main__':
    app.run()
