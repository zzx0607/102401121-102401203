import pytest
from conftest import headers, publish

@pytest.mark.parametrize('kind,label',[('寻物','已找到'),('招领','已归还')])
def test_publish_and_finish(client,data,kind,label):
    data['type']=kind
    response=publish(client,data)
    assert response.status_code==201
    id=response.json['post']['id']
    assert client.get(f'/posts/{id}').status_code==200
    response=client.patch(f'/api/posts/{id}/finish',headers=headers(client))
    assert response.json['post']['status_label']==label
    assert label in client.get('/').text
    assert client.patch(f'/api/posts/{id}/finish',headers=headers(client)).status_code==200

@pytest.mark.parametrize('field',['name','place','contact'])
def test_required(client,data,field):
    data[field]='   '
    assert publish(client,data).status_code==400
    assert client.get('/api/posts').json['posts']==[]

def test_too_long(client,data):
    data['name']='杯'*41
    assert publish(client,data).status_code==400

def test_owner_permissions(app,client,data):
    id=publish(client,data).json['post']['id']
    other=app.test_client()
    for method,url in [('PATCH',f'/api/posts/{id}/finish'),('DELETE',f'/api/posts/{id}')]:
        assert other.open(url,method=method,headers=headers(other)).status_code==403
    assert '蓝色水杯' not in other.get('/my-posts').text
    assert not client.get(f'/api/posts/{id}').json['post']['done']

def test_csrf(client,data):
    client.get('/')
    assert client.post('/api/posts',data=data).status_code==403

def test_delete(client,data):
    id=publish(client,data).json['post']['id']
    assert client.delete(f'/api/posts/{id}',headers=headers(client)).status_code==200
    assert client.get(f'/posts/{id}').status_code==404
    assert client.get('/api/posts').json['posts']==[]

def test_escape_html(client,data):
    data['name']='<script>alert(1)</script>'
    id=publish(client,data).json['post']['id']
    page=client.get(f'/posts/{id}').text
    assert '<script>alert(1)</script>' not in page
    assert '&lt;script&gt;' in page

def test_invalid_category(client,data):
    data['cat']='非法类别'
    assert publish(client,data).status_code==400

def test_pages(client):
    for url in ['/','/publish','/my-posts']:
        assert client.get(url).status_code==200
