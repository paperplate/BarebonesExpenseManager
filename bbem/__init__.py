import os
from flask import Flask
from dotenv import dotenv_values

config = dotenv_values('.env')

def create_app(test_config=None):
    '''create and configure the app.'''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=config['SECRET_KEY'],
        DATABASE=os.path.join(app.instance_path, 'bbem.sqlite'),
        UPLOAD_FOLDER=config['UPLOAD_FOLDER'],
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'hello'


    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import entries
    app.register_blueprint(entries.bp)
    app.add_url_rule('/', endpoint='index')

    return app
