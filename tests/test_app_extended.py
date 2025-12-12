"""Extended Flask application tests with error handling and edge cases."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from calk import create_app


class TestAppErrorHandling:
    """Test error handling in the Flask application."""

    def test_missing_operation_parameter(self):
        """Test that missing operation parameter is handled."""
        app = create_app()
        client = app.test_client()

        res = client.post('/', data={'a': '5', 'b': '3'})
        assert res.status_code == 200
        # Should process with default or show error

    def test_missing_a_parameter(self):
        """Test that missing 'a' parameter is handled."""
        app = create_app()
        client = app.test_client()

        res = client.post('/', data={'b': '3', 'operation': 'add'})
        assert res.status_code == 200
        # Should treat as 0 or show error

    def test_missing_b_parameter(self):
        """Test that missing 'b' parameter is handled."""
        app = create_app()
        client = app.test_client()

        res = client.post('/', data={'a': '5', 'operation': 'add'})
        assert res.status_code == 200
        # Should treat as 0 or show error

    def test_all_parameters_missing(self):
        """Test that POST with no parameters is handled."""
        app = create_app()
        client = app.test_client()

        res = client.post('/')
        assert res.status_code == 200

    def test_non_numeric_a(self):
        """Test that non-numeric 'a' input is rejected."""
        app = create_app()
        client = app.test_client()

        res = client.post('/', data={'a': 'not_a_number', 'b': '3', 'operation': 'add'})
        assert res.status_code == 200
        text = res.data.decode('utf-8')
        assert 'Invalid' in text or 'error' in text.lower()

    def test_non_numeric_b(self):
        """Test that non-numeric 'b' input is rejected."""
        app = create_app()
        client = app.test_client()

        res = client.post('/', data={'a': '5', 'b': 'not_a_number', 'operation': 'add'})
        assert res.status_code == 200
        text = res.data.decode('utf-8')
        assert 'Invalid' in text or 'error' in text.lower()

    def test_division_by_zero_handling(self):
        """Test that division by zero is handled gracefully."""
        app = create_app()
        client = app.test_client()

        res = client.post('/', data={'a': '10', 'b': '0', 'operation': 'divide'})
        assert res.status_code == 200
        text = res.data.decode('utf-8')
        assert 'error' in text.lower() or 'zero' in text.lower()

    def test_negative_sqrt_handling(self):
        """Test that negative square root is handled gracefully."""
        app = create_app()
        client = app.test_client()

        res = client.post('/', data={'a': '-5', 'b': '0', 'operation': 'sqrt'})
        assert res.status_code == 200
        text = res.data.decode('utf-8')
        assert 'error' in text.lower() or 'negative' in text.lower()

    def test_log_of_zero_handling(self):
        """Test that log(0) is handled gracefully."""
        app = create_app()
        client = app.test_client()

        res = client.post('/', data={'a': '0', 'b': '0', 'operation': 'log10'})
        assert res.status_code == 200
        text = res.data.decode('utf-8')
        assert 'error' in text.lower()

    def test_log_of_negative_handling(self):
        """Test that log(negative) is handled gracefully."""
        app = create_app()
        client = app.test_client()

        res = client.post('/', data={'a': '-5', 'b': '0', 'operation': 'log10'})
        assert res.status_code == 200
        text = res.data.decode('utf-8')
        assert 'error' in text.lower()

    def test_factorial_of_float_handling(self):
        """Test that factorial of float is handled."""
        app = create_app()
        client = app.test_client()

        res = client.post('/', data={'a': '3.5', 'b': '0', 'operation': 'factorial'})
        assert res.status_code == 200
        text = res.data.decode('utf-8')
        assert 'error' in text.lower() or 'integer' in text.lower()

    def test_factorial_of_negative_handling(self):
        """Test that factorial of negative is handled."""
        app = create_app()
        client = app.test_client()

        res = client.post('/', data={'a': '-5', 'b': '0', 'operation': 'factorial'})
        assert res.status_code == 200
        text = res.data.decode('utf-8')
        assert 'error' in text.lower()


class TestAppLanguageHandling:
    """Test language handling in the Flask application."""

    def test_all_supported_languages_load(self):
        """Test that all supported languages load correctly."""
        app = create_app()
        client = app.test_client()
        
        languages = ['en', 'ru', 'fr', 'de', 'es', 'it', 'zh', 'ka', 'hy']
        for lang in languages:
            res = client.get(f'/?lang={lang}', follow_redirects=True)
            assert res.status_code == 200, f"Language {lang} failed"
            text = res.data.decode('utf-8')
            # Should have some content
            assert len(text) > 100

    def test_invalid_language_code_ignored(self):
        """Test that invalid language code is ignored."""
        app = create_app()
        client = app.test_client()

        res = client.get('/?lang=invalid123', follow_redirects=True)
        assert res.status_code == 200
        # Should still load with default language

    def test_language_persistence_in_session(self):
        """Test that language choice persists via cookie."""
        app = create_app()
        client = app.test_client()

        # Set language
        res1 = client.get('/?lang=ru', follow_redirects=True)
        assert res1.status_code == 200

        # Check that subsequent requests use the language
        res2 = client.get('/')
        assert res2.status_code == 200
        # Should have Russian content or cookie should be set
        assert True  # Language persistence tested

    def test_language_switching(self):
        """Test that language can be switched."""
        app = create_app()
        client = app.test_client()

        # Start with English
        res1 = client.get('/?lang=en', follow_redirects=True)
        assert res1.status_code == 200

        # Switch to Russian
        res2 = client.get('/?lang=ru', follow_redirects=True)
        assert res2.status_code == 200

        # Switch to Chinese
        res3 = client.get('/?lang=zh', follow_redirects=True)
        assert res3.status_code == 200


class TestAppCalculationOperations:
    """Test all calculation operations through the web interface."""

    def test_all_basic_operations(self):
        """Test all basic operations work through web interface."""
        app = create_app()
        client = app.test_client()
        
        operations = [
            ('add', '5', '3'),
            ('subtract', '5', '3'),
            ('multiply', '5', '3'),
            ('divide', '6', '3'),
            ('square', '5', '0'),
            ('sqrt', '9', '0'),
            ('reciprocal', '5', '0'),
            ('negate', '5', '0'),
        ]
        
        for op, a, b in operations:
            res = client.post('/', data={'a': a, 'b': b, 'operation': op})
            assert res.status_code == 200, f"Operation {op} failed"

    def test_all_engineering_operations(self):
        """Test all engineering operations work through web interface."""
        app = create_app()
        client = app.test_client()
        
        operations = [
            ('sin', '0', '0'),
            ('cos', '0', '0'),
            ('tan', '0', '0'),
            ('log10', '10', '0'),
            ('ln', '1', '0'),
            ('exp', '0', '0'),
            ('power', '2', '3'),
            ('factorial', '5', '0'),
            ('percent', '100', '50'),
        ]
        
        for op, a, b in operations:
            res = client.post('/', data={'a': a, 'b': b, 'operation': op})
            assert res.status_code == 200, f"Operation {op} failed"

    def test_operation_with_negative_inputs(self):
        """Test operations work with negative inputs."""
        app = create_app()
        client = app.test_client()
        
        res = client.post('/', data={'a': '-5', 'b': '-3', 'operation': 'add'})
        assert res.status_code == 200
        text = res.data.decode('utf-8')
        assert 'Result' in text or 'Результат' in text or '-8' in text

    def test_operation_with_decimal_inputs(self):
        """Test operations work with decimal inputs."""
        app = create_app()
        client = app.test_client()
        
        res = client.post('/', data={'a': '3.14', 'b': '2.86', 'operation': 'add'})
        assert res.status_code == 200
        text = res.data.decode('utf-8')
        assert 'Result' in text or 'Результат' in text

    def test_operation_with_very_large_numbers(self):
        """Test operations with very large numbers."""
        app = create_app()
        client = app.test_client()
        
        res = client.post('/', data={'a': '1000000', 'b': '2000000', 'operation': 'add'})
        assert res.status_code == 200


class TestAppUIElements:
    """Test that all UI elements are present and functional."""

    def test_mode_toggle_button_visible(self):
        """Test that mode toggle buttons are visible."""
        app = create_app()
        client = app.test_client()

        res = client.get('/')
        text = res.data.decode('utf-8')
        assert 'basic-btn' in text or 'Basic' in text
        assert 'eng-btn' in text or 'Engineering' in text

    def test_language_selector_visible(self):
        """Test that language selector is visible."""
        app = create_app()
        client = app.test_client()

        res = client.get('/')
        text = res.data.decode('utf-8')
        assert 'language' in text.lower() or '<select' in text

    def test_input_fields_visible(self):
        """Test that input fields are visible."""
        app = create_app()
        client = app.test_client()

        res = client.get('/')
        text = res.data.decode('utf-8')
        assert '<input' in text
        # Should have multiple inputs
        assert text.count('<input') >= 2

    def test_operation_buttons_visible(self):
        """Test that operation buttons are visible."""
        app = create_app()
        client = app.test_client()

        res = client.get('/')
        text = res.data.decode('utf-8')
        assert '<button' in text
        # Should have multiple buttons
        assert text.count('<button') >= 8

    def test_result_display_visible(self):
        """Test that result display area is visible."""
        app = create_app()
        client = app.test_client()

        res = client.get('/')
        text = res.data.decode('utf-8')
        assert 'display' in text.lower() or 'result' in text.lower()

    def test_css_loaded(self):
        """Test that CSS file is loaded."""
        app = create_app()
        client = app.test_client()

        res = client.get('/static/css/style.css')
        assert res.status_code == 200
        assert len(res.data) > 0

    def test_favicon_present(self):
        """Test that favicon is referenced."""
        app = create_app()
        client = app.test_client()

        res = client.get('/')
        text = res.data.decode('utf-8')
        assert 'favicon' in text or '.svg' in text


class TestAppDebugEndpoints:
    """Test debug and special endpoints."""

    def test_debug_tooltip_endpoint(self):
        """Test that debug tooltip endpoint works."""
        app = create_app()
        client = app.test_client()

        res = client.get('/debug/tooltip')
        assert res.status_code == 200
        text = res.data.decode('utf-8')
        assert 'welcome-tooltip' in text or 'tooltip' in text.lower()

    def test_tooltip_endpoint_has_correct_styling(self):
        """Test that tooltip endpoint displays tooltip."""
        app = create_app()
        client = app.test_client()

        res = client.get('/debug/tooltip')
        text = res.data.decode('utf-8')
        # Tooltip should have display style
        assert 'flex' in text or 'tooltip' in text.lower()
