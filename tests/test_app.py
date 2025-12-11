import sys
import os

# ensure project root is on sys.path for test discovery
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from calk import create_app


def test_index_get():
    app = create_app()
    client = app.test_client()

    res = client.get('/')
    assert res.status_code == 200
    text = res.data.decode('utf-8')
    assert 'Calculator' in text or 'Калькулятор' in text


def test_add_operation():
    app = create_app()
    client = app.test_client()

    res = client.post('/', data={'a': '2', 'b': '3', 'operation': 'add'})
    assert res.status_code == 200
    text = res.data.decode('utf-8')
    assert 'Result' in text or 'Результат' in text


def test_language_selector_shows_flags():
    """Test that language selector displays emoji flags"""
    app = create_app()
    client = app.test_client()

    res = client.get('/')
    assert res.status_code == 200
    text = res.data.decode('utf-8')
    
    # Check that emoji flags are present
    assert '🇬🇧' in text  # English flag
    assert '🇷🇺' in text  # Russian flag
    assert '🇫🇷' in text  # French flag
    assert '🇩🇪' in text  # German flag
    assert '🇪🇸' in text  # Spanish flag
    assert '🇮🇹' in text  # Italian flag
    assert '🇨🇳' in text  # Chinese flag
    assert '🇬🇪' in text  # Georgian flag
    assert '🇦🇲' in text  # Armenian flag


def test_georgian_language_support():
    """Test Georgian language is supported and loads correctly"""
    app = create_app()
    client = app.test_client()

    res = client.get('/?lang=ka', follow_redirects=True)
    assert res.status_code == 200
    text = res.data.decode('utf-8')
    assert 'ქართული' in text  # Georgian in page


def test_armenian_language_support():
    """Test Armenian language is supported and loads correctly"""
    app = create_app()
    client = app.test_client()

    res = client.get('/?lang=hy', follow_redirects=True)
    assert res.status_code == 200
    text = res.data.decode('utf-8')
    assert 'Հայերեն' in text  # Armenian in page


def test_mode_buttons_exist():
    """Test that mode buttons (Basic/Engineering) are present"""
    app = create_app()
    client = app.test_client()

    res = client.get('/')
    assert res.status_code == 200
    text = res.data.decode('utf-8')
    assert 'basic-btn' in text
    assert 'eng-btn' in text

