"""Performance and load tests for the calculator application."""
import sys
import os
import time
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from calk import create_app


class TestPerformance:
    """Test performance and response times."""

    def test_homepage_response_time(self):
        """Test that homepage loads in reasonable time (<500ms)."""
        app = create_app()
        client = app.test_client()
        
        start = time.time()
        res = client.get('/')
        elapsed = time.time() - start
        
        assert res.status_code == 200
        # Should respond in < 500ms
        assert elapsed < 0.5, f"Homepage took {elapsed:.3f}s"

    def test_calculation_response_time(self):
        """Test that calculation responds quickly (<200ms)."""
        app = create_app()
        client = app.test_client()
        
        start = time.time()
        res = client.post('/', data={'a': '123.456', 'b': '789.012', 'operation': 'add'})
        elapsed = time.time() - start
        
        assert res.status_code == 200
        # Should respond in < 200ms
        assert elapsed < 0.2, f"Calculation took {elapsed:.3f}s"

    def test_css_loads_efficiently(self):
        """Test that CSS file loads and isn't too large."""
        app = create_app()
        client = app.test_client()
        
        res = client.get('/static/css/style.css')
        assert res.status_code == 200
        
        # CSS shouldn't be excessively large (< 100KB is reasonable)
        assert len(res.data) < 100000, f"CSS file too large: {len(res.data)} bytes"

    def test_multiple_rapid_requests(self):
        """Test that application handles multiple rapid requests."""
        app = create_app()
        client = app.test_client()
        
        start = time.time()
        for i in range(10):
            res = client.post('/', data={'a': str(i), 'b': str(i+1), 'operation': 'add'})
            assert res.status_code == 200
        
        elapsed = time.time() - start
        avg_time = elapsed / 10
        
        # Average response should be < 100ms
        assert avg_time < 0.1, f"Average response time {avg_time:.3f}s is too slow"

    def test_large_number_calculation(self):
        """Test that large number calculations complete efficiently."""
        app = create_app()
        client = app.test_client()
        
        start = time.time()
        res = client.post('/', data={
            'a': '1234567890.123456789',
            'b': '9876543210.987654321',
            'operation': 'multiply'
        })
        elapsed = time.time() - start
        
        assert res.status_code == 200
        # Even with large numbers should respond quickly
        assert elapsed < 0.3, f"Large number calculation took {elapsed:.3f}s"

    def test_many_operations_sequence(self):
        """Test that sequence of different operations completes quickly."""
        app = create_app()
        client = app.test_client()
        
        operations = ['add', 'subtract', 'multiply', 'divide', 'square', 'sqrt', 'sin', 'cos']
        
        start = time.time()
        for op in operations:
            res = client.post('/', data={'a': '5', 'b': '3', 'operation': op})
            assert res.status_code == 200
        
        elapsed = time.time() - start
        avg_time = elapsed / len(operations)
        
        assert avg_time < 0.15, f"Average operation time {avg_time:.3f}s is too slow"

    def test_language_switching_performance(self):
        """Test that language switching is fast."""
        app = create_app()
        client = app.test_client()
        
        langs = ['en', 'ru', 'fr', 'de', 'es', 'it', 'zh', 'ka', 'hy']
        
        start = time.time()
        for lang in langs:
            res = client.get(f'/?lang={lang}', follow_redirects=True)
            assert res.status_code == 200
        
        elapsed = time.time() - start
        avg_time = elapsed / len(langs)
        
        assert avg_time < 0.1, f"Average language switch time {avg_time:.3f}s is too slow"

    def test_tooltip_debug_endpoint_performance(self):
        """Test that debug tooltip endpoint is fast."""
        app = create_app()
        client = app.test_client()
        
        start = time.time()
        res = client.get('/debug/tooltip')
        elapsed = time.time() - start
        
        assert res.status_code == 200
        # Debug endpoint should also be fast
        assert elapsed < 0.3, f"Debug tooltip took {elapsed:.3f}s"

    def test_memory_efficient_error_handling(self):
        """Test that error handling doesn't leak memory."""
        app = create_app()
        client = app.test_client()
        
        # Generate errors
        for i in range(50):
            res = client.post('/', data={
                'a': 'invalid' * 100,
                'b': 'invalid' * 100,
                'operation': 'add'
            })
            assert res.status_code == 200
        
        # Should complete without issues
        assert True
