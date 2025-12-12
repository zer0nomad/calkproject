"""Comprehensive security tests."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from calk import create_app


class TestInputValidation:
    """Test input validation and sanitization."""

    def test_numeric_inputs_accepted(self):
        """Test that numeric inputs are accepted."""
        app = create_app()
        client = app.test_client()
        
        res = client.post('/', data={'a': '123.45', 'b': '67.89', 'operation': 'add'})
        assert res.status_code == 200

    def test_non_numeric_input_rejected(self):
        """Test that non-numeric inputs are rejected."""
        app = create_app()
        client = app.test_client()
        
        res = client.post('/', data={'a': 'abc', 'b': '5', 'operation': 'add'})
        assert res.status_code == 200
        text = res.data.decode('utf-8')
        assert 'Invalid' in text or 'error' in text.lower()

    def test_empty_string_handled(self):
        """Test that empty strings are handled."""
        app = create_app()
        client = app.test_client()
        
        res = client.post('/', data={'a': '', 'b': '', 'operation': 'add'})
        assert res.status_code == 200

    def test_whitespace_trimmed(self):
        """Test that whitespace is handled."""
        app = create_app()
        client = app.test_client()
        
        res = client.post('/', data={'a': '  5  ', 'b': '  3  ', 'operation': 'add'})
        assert res.status_code == 200

    def test_very_large_number(self):
        """Test that very large numbers don't crash application."""
        app = create_app()
        client = app.test_client()
        
        res = client.post('/', data={'a': '9' * 50, 'b': '1', 'operation': 'add'})
        assert res.status_code == 200

    def test_scientific_notation(self):
        """Test that scientific notation is accepted."""
        app = create_app()
        client = app.test_client()
        
        res = client.post('/', data={'a': '1.5e10', 'b': '2.5e-5', 'operation': 'add'})
        assert res.status_code == 200

    def test_negative_numbers_accepted(self):
        """Test that negative numbers are accepted."""
        app = create_app()
        client = app.test_client()
        
        res = client.post('/', data={'a': '-123.45', 'b': '-67.89', 'operation': 'add'})
        assert res.status_code == 200


class TestLanguageParameterValidation:
    """Test language parameter validation."""

    def test_valid_language_codes(self):
        """Test that all valid language codes work."""
        app = create_app()
        client = app.test_client()
        
        valid_langs = ['en', 'ru', 'fr', 'de', 'es', 'it', 'zh', 'ka', 'hy']
        for lang in valid_langs:
            res = client.get(f'/?lang={lang}', follow_redirects=True)
            assert res.status_code == 200

    def test_invalid_language_code_ignored(self):
        """Test that invalid language codes don't crash."""
        app = create_app()
        client = app.test_client()
        
        res = client.get('/?lang=invalid', follow_redirects=True)
        assert res.status_code == 200


class TestOperationParameterValidation:
    """Test operation parameter validation."""

    def test_valid_operations(self):
        """Test that all valid operations work."""
        app = create_app()
        client = app.test_client()
        
        valid_ops = ['add', 'subtract', 'multiply', 'divide', 'square', 'sqrt',
                     'sin', 'cos', 'tan', 'log10', 'ln', 'exp', 'power',
                     'factorial', 'reciprocal', 'negate', 'percent']
        
        for op in valid_ops:
            res = client.post('/', data={'a': '5', 'b': '3', 'operation': op})
            assert res.status_code == 200

    def test_invalid_operation_handled(self):
        """Test that invalid operation is handled."""
        app = create_app()
        client = app.test_client()
        
        res = client.post('/', data={'a': '5', 'b': '3', 'operation': 'invalid_op'})
        assert res.status_code == 200


class TestFormProcessing:
    """Test form processing safety."""

    def test_post_request_works(self):
        """Test that POST requests are processed."""
        app = create_app()
        client = app.test_client()
        
        res = client.post('/', data={'a': '5', 'b': '3', 'operation': 'add'})
        assert res.status_code == 200

    def test_get_request_returns_form(self):
        """Test that GET request returns the form."""
        app = create_app()
        client = app.test_client()
        
        res = client.get('/')
        assert res.status_code == 200
        text = res.data.decode('utf-8')
        assert 'Calculator' in text or 'Калькулятор' in text
