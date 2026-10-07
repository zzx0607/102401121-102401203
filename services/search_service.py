def search_posts(posts, q='', type='', cat='', place='', status=''):
    # Python 字符串匹配，% 和 _ 也作为普通字符处理。
    words = q.strip().casefold().split()
    result = []
    for post in posts:
        haystack = ' '.join(post[k] for k in ('name','cat','place','description')).casefold()
        if not all(word in haystack for word in words):
            continue
        if type and post['type'] != type or cat and post['cat'] != cat:
            continue
        if place.strip().casefold() not in post['place'].casefold():
            continue
        if status == 'active' and post['done'] or status == 'done' and not post['done']:
            continue
        result.append(post)
    return result

def similar_posts(target, posts):
    # 同类别、相反类型且未结束的记录，仅作为参考线索，地点相同优先。
    found = [p for p in posts if p['id'] != target['id'] and not p['done']
             and p['type'] != target['type'] and p['cat'] == target['cat']]
    return sorted(found, key=lambda p:(p['place']==target['place'], p['id']), reverse=True)[:3]
