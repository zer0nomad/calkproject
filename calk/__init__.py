from flask import Flask
from flask_babel import Babel, gettext

babel = Babel()


def create_app(config_object=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Config
    if config_object is None:
        from .config import Config
        app.config.from_object(Config)
    else:
        app.config.from_object(config_object)

    # Initialize extensions
    babel.init_app(app)

    # expose gettext in templates as `gettext` (explicit usage in templates)
    app.jinja_env.globals['gettext'] = gettext

    # register blueprints
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
