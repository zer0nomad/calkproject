from flask import Flask, request
from flask_babel import Babel

babel = Babel()


def get_locale():
    # Check cookie first
    lang = request.cookies.get('lang')
    if lang in ['en', 'ru', 'fr', 'de', 'es', 'it', 'zh', 'ka', 'hy']:
        return lang
    # Then check Accept-Language header
    return request.accept_languages.best_match(['en', 'ru', 'fr', 'de', 'es', 'it', 'zh', 'ka', 'hy']) or 'en'


def create_app(config_object=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Config
    if config_object is None:
        from .config import Config
        app.config.from_object(Config)
    else:
        app.config.from_object(config_object)

    # Initialize extensions
    babel.init_app(app, locale_selector=get_locale)

    # expose gettext in templates
    from flask_babel import gettext as _gettext
    app.jinja_env.globals['gettext'] = _gettext

    # register blueprints
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
