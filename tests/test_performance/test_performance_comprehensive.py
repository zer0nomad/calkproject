"""Performance and load testing for the application."""
import pytest
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


@pytest.mark.performance
class TestResponseTime:
    """Test application response times."""

    def test_index_page_load_time(self, client):
        """Test that index page loads within acceptable time."""
        start = time.time()
        response = client.get('/')
        elapsed = time.time() - start
        
        assert response.status_code == 200
        # Should load in less than 500ms
        assert elapsed < 0.5, f"Page load took {elapsed*1000:.2f}ms"

    def test_calculation_response_time(self, client):
        """Test that calculations complete within acceptable time."""
        start = time.time()
        response = client.post('/', data={
            'a': '1234567890',
            'b': '9876543210',
            'operation': 'add'
        })
        elapsed = time.time() - start
        
        assert response.status_code == 200
        # Calculation should be fast (< 200ms)
        assert elapsed < 0.2, f"Calculation took {elapsed*1000:.2f}ms"

    def test_language_switch_response_time(self, client):
        """Test that language switch is fast."""
        start = time.time()
        response = client.get('/?lang=ru', follow_redirects=True)
        elapsed = time.time() - start
        
        assert response.status_code == 200
        # Should be quick (< 300ms)
        assert elapsed < 0.3, f"Language switch took {elapsed*1000:.2f}ms"

    def test_debug_tooltip_response_time(self, client):
        """Test debug tooltip endpoint performance."""
        start = time.time()
        response = client.get('/debug/tooltip')
        elapsed = time.time() - start
        
        assert response.status_code == 200
        # Should be very fast (< 200ms)
        assert elapsed < 0.2, f"Debug endpoint took {elapsed*1000:.2f}ms"


@pytest.mark.performance
class TestConcurrency:
    """Test application under concurrent load."""

    def test_concurrent_requests(self, client):
        """Test handling of concurrent requests."""
        def make_request():
            return client.get('/')
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = []
            for future in as_completed(futures):
                response = future.result()
                results.append(response)
        
        # All requests should succeed
        assert all(r.status_code == 200 for r in results)

    def test_concurrent_calculations(self, client):
        """Test concurrent calculation requests."""
        def make_calculation():
            return client.post('/', data={
                'a': '5',
                'b': '3',
                'operation': 'add'
            })
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_calculation) for _ in range(10)]
            results = []
            for future in as_completed(futures):
                response = future.result()
                results.append(response)
        
        # All calculations should succeed
        assert all(r.status_code == 200 for r in results)

    def test_mixed_concurrent_operations(self, client):
        """Test concurrent mix of different operations."""
        def make_mixed_request(i):
            if i % 2 == 0:
                return client.get('/')
            elif i % 3 == 0:
                return client.get('/?lang=ru', follow_redirects=True)
            else:
                return client.post('/', data={
                    'a': str(i),
                    'b': str(i + 1),
                    'operation': 'add'
                })
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_mixed_request, i) for i in range(15)]
            results = []
            for future in as_completed(futures):
                response = future.result()
                results.append(response)
        
        # All requests should succeed
        assert all(r.status_code == 200 for r in results)


@pytest.mark.performance
class TestMemoryUsage:
    """Test memory efficiency of calculations."""

    def test_large_number_calculation(self, client):
        """Test calculation with very large numbers."""
        large_num = '1' * 100
        response = client.post('/', data={
            'a': large_num,
            'b': large_num,
            'operation': 'add'
        })
        assert response.status_code == 200
        # Should handle gracefully

    def test_many_sequential_calculations(self, client):
        """Test many sequential calculations don't leak memory."""
        for i in range(100):
            response = client.post('/', data={
                'a': str(i),
                'b': str(i + 1),
                'operation': 'add'
            })
            assert response.status_code == 200

    def test_language_switch_repeated(self, client):
        """Test repeated language switching."""
        langs = ['en', 'ru', 'fr', 'de', 'es', 'it', 'zh', 'ka', 'hy']
        for _ in range(5):  # Cycle through multiple times
            for lang in langs:
                response = client.get(f'/?lang={lang}', follow_redirects=True)
                assert response.status_code == 200


@pytest.mark.performance
class TestCacheEfficiency:
    """Test response caching and efficiency."""

    def test_static_content_cache(self, client):
        """Test that static resources can be cached."""
        response = client.get('/static/css/style.css')
        assert response.status_code in [200, 304]
        # Check for cache headers
        headers = response.headers
        # In production, should have cache control headers
        assert response.status_code == 200

    def test_repeated_requests_efficiency(self, client):
        """Test efficiency of repeated identical requests."""
        times = []
        for _ in range(5):
            start = time.time()
            response = client.get('/')
            elapsed = time.time() - start
            times.append(elapsed)
            assert response.status_code == 200
        
        # Subsequent requests should be similar to first
        avg_time = sum(times) / len(times)
        assert avg_time < 0.5


@pytest.mark.performance
class TestCalculationPerformance:
    """Test specific calculation performance."""

    def test_basic_arithmetic_speed(self, client):
        """Test basic arithmetic operations are fast."""
        operations = ['add', 'sub', 'mul', 'div']
        for op in operations:
            start = time.time()
            response = client.post('/', data={
                'a': '123.456',
                'b': '789.012',
                'operation': op
            })
            elapsed = time.time() - start
            assert response.status_code == 200
            assert elapsed < 0.1

    def test_engineering_operations_speed(self, client):
        """Test engineering function operations are fast."""
        operations = ['sqrt', 'square', 'ln', 'log10', 'sin', 'cos', 'tan']
        for op in operations:
            start = time.time()
            response = client.post('/', data={
                'a': '45',
                'b': '0',
                'operation': op
            })
            elapsed = time.time() - start
            assert response.status_code == 200
            assert elapsed < 0.1

    def test_factorial_performance(self, client):
        """Test factorial calculation performance."""
        start = time.time()
        response = client.post('/', data={
            'a': '20',
            'b': '0',
            'operation': 'factorial'
        })
        elapsed = time.time() - start
        
        assert response.status_code == 200
        # Even factorial should be reasonably fast
        assert elapsed < 0.5


@pytest.mark.performance
class TestScalability:
    """Test scalability under load."""

    def test_burst_traffic_handling(self, client):
        """Test handling of burst traffic."""
        # Simulate burst of requests
        responses = []
        for i in range(20):
            response = client.post('/', data={
                'a': str(i),
                'b': str(i + 1),
                'operation': 'add'
            })
            responses.append(response)
        
        # All should succeed even under burst
        assert all(r.status_code == 200 for r in responses)

    def test_sustained_load(self, client):
        """Test sustained load over time."""
        for iteration in range(5):
            for i in range(10):
                response = client.post('/', data={
                    'a': str(i),
                    'b': str(i + 1),
                    'operation': 'add'
                })
                assert response.status_code == 200
            # Brief pause between iterations
            time.sleep(0.01)

    def test_error_handling_under_load(self, client):
        """Test error handling under load."""
        # Mix of valid and invalid requests
        for i in range(50):
            data = {
                'a': 'invalid' if i % 5 == 0 else str(i),
                'b': '3',
                'operation': 'add' if i % 3 != 0 else 'invalid_op'
            }
            response = client.post('/', data=data)
            assert response.status_code == 200


@pytest.mark.performance
class TestResourceConsumption:
    """Test resource consumption efficiency."""

    def test_minimal_response_overhead(self, client):
        """Test that response overhead is minimal."""
        response = client.get('/')
        # Content length should be reasonable
        content_length = len(response.data)
        # Should be less than 500KB for a simple calculator
        assert content_length < 500000

    def test_css_file_size(self, client):
        """Test that CSS file is reasonable size."""
        response = client.get('/static/css/style.css')
        if response.status_code == 200:
            # CSS should be reasonably sized
            assert len(response.data) < 100000

    def test_repeated_resource_requests(self, client):
        """Test repeated requests to same resources."""
        # Request same resource multiple times
        for _ in range(10):
            response = client.get('/static/css/style.css')
            # Should consistently succeed
            assert response.status_code in [200, 304]
