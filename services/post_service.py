import models
CATEGORIES = ('证件', '钥匙', '水杯', '雨伞', '耳机', '书籍', '其他')
class PostError(ValueError):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status

def validate_post(raw):
    limits = {'name':40, 'place':60, 'contact':80, 'time':40, 'description':500}
    result = {}
    for key, limit in limits.items():
        value = raw.get(key, '')
        if not isinstance(value, str):
            raise PostError('字段必须为文字')
        result[key] = value.strip()
        if len(result[key]) > limit:
            raise PostError(f'{key} 超出 {limit} 字限制')
    for key, label in [('name','物品名称'), ('place','地点'), ('contact','联系方式')]:
        if not result[key]:
            raise PostError(f'请填写{label}')
    result['type'] = raw.get('type', '')
    result['cat'] = raw.get('cat', '其他')
    if result['type'] not in ('寻物', '招领'):
        raise PostError('请选择寻物或招领')
    if result['cat'] not in CATEGORIES:
        raise PostError('物品类别不正确')
    return result

def require_post(post_id):
    post = models.get_post(post_id)
    if post is None:
        raise PostError('这条信息不存在或已删除', 404)
    return post

def require_owner(post_id, owner_id):
    post = require_post(post_id)
    if post['owner_id'] != owner_id:
        raise PostError('只有发布者可以修改这条信息', 403)
    return post

def finish(post_id, owner_id):
    require_owner(post_id, owner_id)
    models.finish_post(post_id, owner_id)
    return require_post(post_id)

def status_label(post):
    if post['done']:
        return '已找到' if post['type'] == '寻物' else '已归还'
    return post['type']
