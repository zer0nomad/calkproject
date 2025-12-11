import os

class Config:
    SECRET_KEY = 'dev-secret'
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    # Get the parent directory of this file (which is calk/), then go up to get project root
    _BASEDIR = os.path.abspath(os.path.dirname(__file__))
    BABEL_TRANSLATION_DIRECTORIES = os.path.join(os.path.dirname(_BASEDIR), 'translations')
    LANGUAGES = {
        'en': 'English 🇬🇧',
        'ru': 'Русский 🇷🇺',
        'fr': 'Français 🇫🇷',
        'de': 'Deutsch 🇩🇪',
        'es': 'Español 🇪🇸',
        'it': 'Italiano 🇮🇹',
        'zh': '中文 🇨🇳',
        'ka': 'ქართული 🇬🇪',
        'hy': 'Հայերեն 🇦🇲'
    }
