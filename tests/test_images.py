from io import BytesIO
from pathlib import Path
from PIL import Image
from conftest import headers, publish

def test_real_image(app,client,data):
    image=BytesIO();Image.new('RGB',(20,20),'purple').save(image,'PNG');image.seek(0)
    data['image']=(image,'../../unsafe.png')
    response=publish(client,data)
    assert response.status_code==201
    post=response.json['post'];name=post['image']
    assert '/' not in name and name.endswith('.jpg')
    assert client.get('/uploads/'+name).status_code==200
    client.delete('/api/posts/'+str(post['id']),headers=headers(client))
    assert not (Path(app.config['UPLOAD_FOLDER'])/name).exists()

def test_fake_image(client,data):
    data['image']=(BytesIO(b'<script>bad</script>'),'fake.png')
    assert publish(client,data).status_code==400

def test_large_image(client,data):
    data['image']=(BytesIO(b'x'*(5*1024*1024+1)),'large.png')
    assert publish(client,data).status_code==400

def test_body_limit(client,data):
    data['image']=(BytesIO(b'x'*(7*1024*1024)),'huge.png')
    assert publish(client,data).status_code==413
