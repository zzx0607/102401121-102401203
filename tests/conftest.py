import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pytest
from app import create_app

@pytest.fixture
def app(tmp_path):
    return create_app({'TESTING':True, 'SECRET_KEY':'test-only',
        'DATABASE':str(tmp_path/'test.db'), 'UPLOAD_FOLDER':str(tmp_path/'uploads')})

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def data():
    return {'type':'寻物','name':'蓝色水杯','cat':'水杯','place':'明理楼 B203',
            'time':'10月5日','description':'小熊贴纸','contact':'demo_contact'}

def headers(client):
    client.get('/')
    with client.session_transaction() as session:
        return {'X-CSRF-Token':session['csrf_token']}

def publish(client, data):
    return client.post('/api/posts',data=data,headers=headers(client))
