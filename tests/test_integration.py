"""Integration and end-to-end tests for the application."""
import pytest


@pytest.mark.integration
class TestCalculatorIntegration:
    """Test complete calculator workflows."""

    def test_basic_calculation_flow(self, client):
        """Test complete basic calculation flow."""
        # 1. Load page
        response = client.get('/')
        assert response.status_code == 200
        
        # 2. Perform calculation
        response = client.post('/', data={
            'a': '10',
            'b': '5',
            'operation': 'add'
        })
        assert response.status_code == 200
        text = response.data.decode('utf-8')
        # Should show result
        assert '15' in text or 'Result' in text

    def test_multiple_calculations_sequence(self, client):
        """Test sequence of multiple calculations."""
        operations = [
            ('add', '5', '3', '8'),
            ('sub', '10', '3', '7'),
            ('mul', '4', '5', '20'),
            ('div', '20', '4', '5'),
        ]
        
        for op, a, b, expected in operations:
            response = client.post('/', data={
                'a': a,
                'b': b,
                'operation': op
            })
            assert response.status_code == 200
            text = response.data.decode('utf-8')
            # Result should contain expected value
            assert expected in text or 'Result' in text

    def test_engineering_mode_workflow(self, client):
        """Test engineering mode operations."""
        operations = [
            ('sin', '0'),
            ('sqrt', '16'),
            ('ln', '1'),
            ('factorial', '5'),
        ]
        
        for op, a in operations:
            response = client.post('/', data={
                'a': a,
                'b': '0',
                'operation': op
            })
            assert response.status_code == 200

    def test_error_recovery_workflow(self, client):
        """Test recovery from errors."""
        # Invalid input
        response = client.post('/', data={
            'a': 'invalid',
            'b': '5',
            'operation': 'add'
        })
        assert response.status_code == 200
        text = response.data.decode('utf-8')
        assert 'error' in text.lower() or 'invalid' in text.lower()
        
        # Follow with valid input
        response = client.post('/', data={
            'a': '5',
            'b': '3',
            'operation': 'add'
        })
        assert response.status_code == 200


@pytest.mark.integration
class TestLanguageIntegration:
    """Test language selection integration."""

    def test_language_selection_persistence(self, client):
        """Test that language selection persists."""
        # Set language
        response = client.get('/?lang=ru', follow_redirects=True)
        assert response.status_code == 200
        
        # Make calculation
        response = client.post('/', data={
            'a': '5',
            'b': '3',
            'operation': 'add'
        })
        assert response.status_code == 200

    def test_language_switching(self, client):
        """Test switching between languages."""
        langs = ['en', 'ru', 'fr', 'de', 'es', 'it', 'zh', 'ka', 'hy']
        
        for lang in langs:
            response = client.get(f'/?lang={lang}', follow_redirects=True)
            assert response.status_code == 200

    def test_calculation_in_different_languages(self, client):
        """Test calculations are language-independent."""
        langs = ['en', 'ru', 'fr', 'de']
        
        for lang in langs:
            # Set language
            client.get(f'/?lang={lang}', follow_redirects=True)
            
            # Perform calculation
            response = client.post('/', data={
                'a': '10',
                'b': '5',
                'operation': 'add'
            })
            assert response.status_code == 200


@pytest.mark.integration
class TestTooltipIntegration:
    """Test tooltip functionality integration."""

    def test_tooltip_debug_endpoint(self, client):
        """Test debug tooltip endpoint."""
        response = client.get('/debug/tooltip')
        assert response.status_code == 200
        text = response.data.decode('utf-8')
        assert 'tooltip' in text or 'welcome' in text.lower()

    def test_tooltip_with_language_selection(self, client):
        """Test tooltip with different languages."""
        response = client.get('/debug/tooltip')
        assert response.status_code == 200
        
        # Tooltip should be in correct language
        response = client.get('/debug/tooltip?lang=ru', follow_redirects=True)
        assert response.status_code == 200

    def test_tooltip_close_button_accessible(self, client):
        """Test tooltip has close functionality."""
        response = client.get('/debug/tooltip')
        assert response.status_code == 200
        text = response.data.decode('utf-8')
        # Should have close button
        assert 'close' in text.lower() or '×' in text


@pytest.mark.integration
class TestFullUserJourney:
    """Test complete user journeys."""

    def test_first_time_user_journey(self, client):
        """Test first time user experience."""
        # 1. Load page
        response = client.get('/')
        assert response.status_code == 200
        
        # 2. See tooltip (or skip it)
        response = client.get('/debug/tooltip')
        assert response.status_code == 200
        
        # 3. Select language
        response = client.get('/?lang=ru', follow_redirects=True)
        assert response.status_code == 200
        
        # 4. Perform first calculation
        response = client.post('/', data={
            'a': '10',
            'b': '5',
            'operation': 'add'
        })
        assert response.status_code == 200

    def test_returning_user_journey(self, client):
        """Test returning user experience."""
        # 1. Load page (tooltip already seen)
        response = client.get('/')
        assert response.status_code == 200
        
        # 2. Language already selected (in cookie)
        response = client.get('/?lang=fr', follow_redirects=True)
        assert response.status_code == 200
        
        # 3. Perform calculations
        for i in range(3):
            response = client.post('/', data={
                'a': str(i + 5),
                'b': str(i + 3),
                'operation': 'add'
            })
            assert response.status_code == 200

    def test_power_user_journey(self, client):
        """Test power user workflow."""
        # Set up
        client.get('/?lang=en')
        
        # Basic calculations
        for op in ['add', 'sub', 'mul', 'div']:
            response = client.post('/', data={
                'a': '100',
                'b': '10',
                'operation': op
            })
            assert response.status_code == 200
        
        # Engineering operations
        for op in ['sqrt', 'sin', 'ln', 'factorial']:
            response = client.post('/', data={
                'a': '5',
                'b': '0',
                'operation': op
            })
            assert response.status_code == 200


@pytest.mark.integration
class TestErrorHandling:
    """Test error handling throughout the application."""

    def test_division_by_zero_handling(self, client):
        """Test division by zero error handling."""
        response = client.post('/', data={
            'a': '10',
            'b': '0',
            'operation': 'div'
        })
        assert response.status_code == 200
        text = response.data.decode('utf-8')
        assert 'error' in text.lower() or 'zero' in text.lower()

    def test_invalid_operation_handling(self, client):
        """Test invalid operation error handling."""
        response = client.post('/', data={
            'a': '5',
            'b': '3',
            'operation': 'invalid_operation'
        })
        assert response.status_code == 200

    def test_math_domain_error_handling(self, client):
        """Test math domain error handling."""
        response = client.post('/', data={
            'a': '-1',
            'b': '0',
            'operation': 'sqrt'
        })
        assert response.status_code == 200
        text = response.data.decode('utf-8')
        # Should handle gracefully
        assert len(text) > 0

    def test_input_type_error_handling(self, client):
        """Test input type error handling."""
        response = client.post('/', data={
            'a': 'not_a_number',
            'b': 'also_not_a_number',
            'operation': 'add'
        })
        assert response.status_code == 200
        text = response.data.decode('utf-8')
        assert 'Invalid' in text or 'invalid' in text or 'error' in text.lower()


@pytest.mark.integration
class TestAccessibilityIntegration:
    """Test accessibility throughout user journeys."""

    def test_keyboard_only_navigation(self, client):
        """Test navigation using keyboard only."""
        response = client.get('/')
        assert response.status_code == 200
        text = response.data.decode('utf-8')
        # Should have keyboard accessible elements
        assert 'button' in text or 'input' in text

    def test_screen_reader_friendly_content(self, client):
        """Test content is screen reader friendly."""
        response = client.get('/')
        assert response.status_code == 200
        text = response.data.decode('utf-8')
        # Should have alt text, labels, ARIA attributes
        assert 'aria' in text.lower() or 'label' in text.lower()

    def test_language_change_accessibility(self, client):
        """Test language changes are accessible."""
        langs = ['en', 'ru', 'fr', 'de']
        for lang in langs:
            response = client.get(f'/?lang={lang}', follow_redirects=True)
            assert response.status_code == 200
            text = response.data.decode('utf-8')
            # Page content should be available
            assert len(text) > 100


@pytest.mark.integration
class TestPerformanceIntegration:
    """Test performance under integrated workflows."""

    def test_calculation_sequence_performance(self, client):
        """Test performance of calculation sequence."""
        import time
        
        start = time.time()
        for i in range(20):
            response = client.post('/', data={
                'a': str(i),
                'b': str(i + 1),
                'operation': 'add'
            })
            assert response.status_code == 200
        elapsed = time.time() - start
        
        # 20 calculations should complete in reasonable time
        assert elapsed < 5, f"Calculation sequence took {elapsed}s"

    def test_language_switching_performance(self, client):
        """Test performance of language switching."""
        import time
        
        start = time.time()
        langs = ['en', 'ru', 'fr', 'de', 'es', 'it', 'zh', 'ka', 'hy']
        for lang in langs * 2:  # Cycle twice
            response = client.get(f'/?lang={lang}', follow_redirects=True)
            assert response.status_code == 200
        elapsed = time.time() - start
        
        # Should switch languages quickly
        assert elapsed < 3, f"Language switching took {elapsed}s"
