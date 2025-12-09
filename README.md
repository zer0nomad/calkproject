# calkproject

Веб-приложение — научный калькулятор на Flask, демонстрирующее лучшие практики разработки:
- **Application Factory** для управления конфигурацией
- **Service Layer** для отделения бизнес-логики от Flask
- **TDD** с полным покрытием тестами (23 теста)
- **i18n** с поддержкой русского и английского языков
- **Retro UI** в стиле Elektronika MK-85 (80-е годы)

## Структура проекта

```
calkproject/
├── calk/                              # Основной пакет приложения
│   ├── __init__.py                    # Application Factory (create_app)
│   ├── services/
│   │   └── calculator_service.py      # Бизнес-логика (чистый Python)
│   ├── routes/
│   │   └── main.py                    # Flask Blueprint маршруты
│   ├── templates/
│   │   └── index.html                 # HTML шаблон с режимом Basic/Engineering
│   └── static/
│       ├── css/
│       │   └── style.css              # Retro 80s стилизация
│       └── img/
│           └── favicon.svg            # SVG favicon Elektronika MK-85
├── translations/                      # i18n переводы (en, ru)
│   ├── en/LC_MESSAGES/
│   │   ├── messages.po                # Английские строки
│   │   └── messages.mo                # Скомпилированные переводы
│   └── ru/LC_MESSAGES/
│       ├── messages.po                # Русские переводы
│       └── messages.mo                # Скомпилированные переводы
├── tests/                             # Unit и интеграционные тесты
│   ├── test_calculator_service.py     # Тесты бизнес-логики (23 теста)
│   └── test_app.py                    # Тесты Flask приложения
├── run.py                             # Точка входа (запуск сервера)
└── requirements.txt                   # Зависимости Python
```

## Быстрый старт

### 1. Установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate  # На Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Запуск приложения

```bash
python run.py
```

Приложение будет доступно по адресу: **http://127.0.0.1:5000**

### 3. Запуск тестов

```bash
pytest -v
# или кратко:
pytest -q
```

## Функциональность

### Режим Basic (основные операции)

| Кнопка | Операция | Функция |
|--------|----------|---------|
| `+` | Сложение | `a + b` |
| `−` | Вычитание | `a - b` |
| `×` | Умножение | `a × b` |
| `÷` | Деление | `a ÷ b` |
| `x²` | Квадрат | `a²` |
| `√` | Корень квадратный | `√a` |
| `1/x` | Обратное число | `1/a` |
| `+/−` | Изменение знака | `−a` |

### Режим Engineering (научные функции)

| Кнопка | Операция | Функция |
|--------|----------|---------|
| `sin` | Синус | `sin(a°)` |
| `cos` | Косинус | `cos(a°)` |
| `tan` | Тангенс | `tan(a°)` |
| `log` | Логарифм по основанию 10 | `log₁₀(a)` |
| `ln` | Натуральный логарифм | `ln(a)` |
| `eˣ` | Экспонента | `e^a` |
| `n!` | Факториал | `a!` |
| `aˣ` | Степень | `a^b` |
| `%` | Процент | `a / 100` |
| `π` | Число Пи | `π` |
| `e` | Число Эйлера | `e` |

## Архитектура

### Service Layer (`calk/services/calculator_service.py`)

Чистая Python логика, независимая от Flask:

```python
def add(a: float, b: float) -> float:
    return a + b

def sin(a: float, in_degrees: bool = True) -> float:
    """Синус функция (в градусах по умолчанию)"""
    rad = radians(a) if in_degrees else a
    return _sin(rad)
```

**Преимущества:**
- Легко тестировать (без Flask зависимостей)
- Переиспользуемо в других проектах
- Понятная обработка ошибок

### Application Factory (`calk/__init__.py`)

```python
def create_app():
    app = Flask(__name__)
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    babel.init_app(app)
    
    from .routes import main_bp
    app.register_blueprint(main_bp)
    return app
```

**Преимущества:**
- Упрощает тестирование (отдельная app для каждого теста)
- Поддерживает множество конфигураций
- Чистая изоляция

### Routes (`calk/routes/main.py`)

Flask Blueprint контроллер:

```python
@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        op = request.form.get('operation')
        a = float(request.form.get('a', 0))
        b = float(request.form.get('b', 0))
        
        if op == 'add':
            result = svc.add(a, b)
        # ... другие операции
    return render_template('index.html', result=result, error=error)
```

## Переводы (i18n)

Приложение поддерживает английский (en) и русский (ru) языки.

### Как добавить новую строку перевода

1. Добавьте в шаблон или код:
```python
from flask_babel import gettext
message = gettext('Hello, World!')
```

2. Соберите строки:
```bash
pybabel extract -F babel.cfg -o messages.pot .
```

3. Обновите переводы:
```bash
pybabel update -i messages.pot -d translations
```

4. Отредактируйте файлы `.po` и скомпилируйте:
```bash
pybabel compile -d translations
```

## Тестирование

### Полный список тестов (23 шт.)

#### Интеграционные тесты (2)

```
test_app.py::test_index_get          ✓ Проверка загрузки главной страницы
test_app.py::test_add_operation      ✓ Проверка операции сложения через форму
```

#### Unit тесты бизнес-логики (21)

**Базовые операции (6):**
```
test_calculator_service.py::test_add            ✓ 1 + 2 = 3
test_calculator_service.py::test_sub            ✓ 5 - 3 = 2
test_calculator_service.py::test_mul            ✓ 2 × 3 = 6
test_calculator_service.py::test_div            ✓ 10 ÷ 2 = 5
test_calculator_service.py::test_div_by_zero    ✓ Деление на ноль вызывает исключение
test_calculator_service.py::test_square         ✓ 4² = 16
```

**Корни и степени (3):**
```
test_calculator_service.py::test_sqrt           ✓ √9 = 3
test_calculator_service.py::test_sqrt_negative  ✓ √(-4) вызывает исключение
test_calculator_service.py::test_power          ✓ 2³ = 8, 5⁰ = 1
```

**Тригонометрия (3):**
```
test_calculator_service.py::test_sin            ✓ sin(0°) = 0, sin(90°) = 1
test_calculator_service.py::test_cos            ✓ cos(0°) = 1, cos(90°) = 0
test_calculator_service.py::test_tan            ✓ tan(0°) = 0
```

**Логарифмы и экспонента (3):**
```
test_calculator_service.py::test_log10          ✓ log₁₀(10) = 1, log₁₀(100) = 2
test_calculator_service.py::test_ln             ✓ ln(e) = 1
test_calculator_service.py::test_exp            ✓ e⁰ = 1, e¹ = e
```

**Утилиты (4):**
```
test_calculator_service.py::test_factorial      ✓ 5! = 120, 0! = 1
test_calculator_service.py::test_reciprocal     ✓ 1/2 = 0.5, 1/0.5 = 2
test_calculator_service.py::test_reciprocal_zero ✓ 1/0 вызывает исключение
test_calculator_service.py::test_percent        ✓ 50% = 0.5, 100% = 1
```

**Специальные (2):**
```
test_calculator_service.py::test_negate         ✓ -5 = -5, -(-3) = 3
test_calculator_service.py::test_constants      ✓ π ≈ 3.14159, e ≈ 2.71828
```

### Запуск тестов с покрытием

```bash
pytest --cov=calk tests/
```

## Обработка ошибок

Приложение корректно обрабатывает ошибки:

| Ошибка | Обработка |
|--------|-----------|
| Деление на ноль | `DivisionByZeroError` |
| Корень отрицательного числа | `CalculatorError` |
| Логарифм неположительного числа | `CalculatorError` |
| Факториал дробного числа | `CalculatorError` |
| Некорректный ввод | Сообщение об ошибке в UI |

## Стиль и дизайн

### Retro 80s Theme

Калькулятор стилизован под советский калькулятор **Elektronika MK-85**:

- **Цветовая палитра:**
  - Основной цвет: Beige (#d4af9a)
  - LCD дисплей: Dark Green (#1a3a2a) с зеленым текстом (#00ff41)
  - Кнопки: Tan (#a89888) с коричневыми тенями

- **Шрифт:** Courier New (моноширина) для аутентичного вида

- **Эффекты:**
  - Физическое нажатие кнопок (translateY)
  - LCD свечение текста (text-shadow)
  - Вдавленные тени для объема

### Адаптивность

- **Desktop:** 4 колонки кнопок
- **Tablet:** 3 колонки кнопок
- **Mobile:** Стекируется на 100% ширину

## Технологический стек

| Компонент | Версия | Назначение |
|-----------|--------|-----------|
| Python | 3.12+ | Язык программирования |
| Flask | 3.1.2 | Web-фреймворк |
| Flask-Babel | 4.0.0 | i18n поддержка |
| pytest | 9.0.2 | Testing framework |

## Лицензия

MIT

## Примечания

Этот проект служит демонстрацией лучших практик разработки веб-приложений на Python:
- Разделение ответственности (MVC, Service Layer)
- Testability (чистая архитектура)
- Интернационализация (i18n)
- Retro UI design (CSS3)
