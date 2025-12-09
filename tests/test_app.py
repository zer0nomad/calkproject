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
