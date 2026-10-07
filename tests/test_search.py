from conftest import publish, headers
from services.search_service import search_posts, similar_posts

def test_keyword_and_filters(client,data):
    publish(client,data)
    assert len(client.get('/api/posts?q=小熊').json['posts'])==1
    assert len(client.get('/api/posts?cat=水杯&place=明理楼&type=寻物').json['posts'])==1
    assert client.get('/api/posts?q=不存在').json['posts']==[]
    assert client.get('/api/posts?type=招领').json['posts']==[]
    assert client.get('/api/posts?q=%25').json['posts']==[]

def test_status(client,data):
    id=publish(client,data).json['post']['id']
    client.patch(f'/api/posts/{id}/finish',headers=headers(client))
    assert client.get('/api/posts?status=active').json['posts']==[]
    assert len(client.get('/api/posts?status=done').json['posts'])==1

def test_case_and_whitespace(data):
    data.update(id=1, done=0, name='USB 耳机')
    assert search_posts([data],q='  usb   耳机 ')==[data]

def test_similar(data):
    target=dict(data,id=1,done=0)
    match=dict(data,id=2,type='招领',done=0)
    ended=dict(match,id=3,done=1)
    same_type=dict(target,id=4)
    other_category=dict(match,id=5,cat='书籍')
    assert similar_posts(target,[target,match,ended,same_type,other_category])==[match]
