from io import BytesIO
from pathlib import Path
from uuid import uuid4
import warnings
from PIL import Image, UnidentifiedImageError
from flask import current_app
from services.post_service import PostError

def save_image(upload):
    if not upload or not upload.filename:
        return None
    content = upload.read(current_app.config['MAX_IMAGE_BYTES'] + 1)
    if len(content) > current_app.config['MAX_IMAGE_BYTES']:
        raise PostError('图片不能超过 5MB')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(BytesIO(content)) as im:
                if im.format not in ('JPEG','PNG','WEBP'):
                    raise PostError('仅支持 JPG、PNG、WebP 图片')
                if im.width * im.height > 20_000_000:
                    raise PostError('图片像素过大，请压缩后上传')
                im.verify()
            with Image.open(BytesIO(content)) as im:
                im.load()
                clean = im.convert('RGB')
                clean.thumbnail((1600,1600))
                name = uuid4().hex + '.jpg'
                clean.save(Path(current_app.config['UPLOAD_FOLDER']) / name, 'JPEG', quality=88)
        return name
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        if isinstance(exc, PostError):
            raise
        raise PostError('无法读取图片，请选择有效的 JPG、PNG、WebP 文件') from exc

def remove_image(name):
    if name:
        (Path(current_app.config['UPLOAD_FOLDER']) / name).unlink(missing_ok=True)
