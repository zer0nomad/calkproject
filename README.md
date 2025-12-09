# calkproject

Пример проекта — веб-калькулятор на Flask с использованием паттерна Application Factory,
Service Layer и поддержкой i18n через Flask-Babel.

Что внутри:
- `calk/` — пакет приложения
- `calk/services/calculator_service.py` — бизнес-логика (независимая от Flask)
- `calk/routes/main.py` — контроллеры / маршруты
- `calk/templates/index.html` — простой шаблон калькулятора с i18n
- `translations/` — каталоги переводов (en, ru)
- `tests/` — unit и интеграционные тесты

Установка зависимостей:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Запуск приложения (локально):

```bash
python run.py
# приложение будет доступно по адресу http://127.0.0.1:5000
```

Переводы:
- Файлы `.po` находятся в `translations/<lang>/LC_MESSAGES/messages.po`.
- Перед использованием на проде скомпилируйте перевод в `.mo`:

```bash
pip install Babel
pybabel compile -d translations
```

Тесты:

```bash
pytest -q
```

Замечания по архитектуре:
- Вся бизнес-логика вынесена в `calk/services` и легко тестируема.
- `create_app()` реализует фабрику приложений, упрощающую тестирование.
- Контроллеры только парсят вход, вызывают сервис и возвращают представление.
