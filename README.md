# 拾光 · 校园失物招领（Python 版）

可在本地运行的 Flask + SQLite 完整源码。Python 3.10 及以上，无需 Node.js 或 MySQL。

## Windows 启动

解压后，在 campus-lost-found 文件夹内打开终端：

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

浏览器打开 http://127.0.0.1:5000 。保持终端运行，按 Ctrl+C 停止。
如果电脑没有 `py` 命令，第一行使用 `python -m venv .venv`。

## macOS / Linux 启动

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

## 已实现

- 发布寻物启事和失物招领，必填、长度、类型及日期校验。
- 首页按关键词、类型、分类和状态搜索，按最新发布排序。
- 图片预览、移除、上传；支持 JPG/PNG/WebP，最大 5MB、2000 万像素；重新编码为 JPEG。
- 详情页按需读取联系方式，显示相同分类、类型相反的线索。
- 我的发布仅列出当前浏览器身份的记录，后端检查状态修改权限。
- 标记已找到/已归还；重复请求保持已结束状态。
- SQLite 持久化，Session 签名、CSRF 校验、SQL 参数化和模板自动转义。
- 搜索条件随 URL 保存，详情返回列表时恢复滚动位置。

## 代码怎么读

1. `app.py`：创建 Flask、配置 Session、注册路由、初始化数据库。
2. `routes/pages.py`：返回 HTML 页面。
3. `routes/posts.py`：接收浏览器数据并返回 JSON。
4. `services/post_service.py`：校验输入。
5. `models.py`：执行增查改 SQL。
6. `database.py`：连接 SQLite、创建 posts 表、请求结束时关闭连接。
7. `templates/` 和 `static/`：页面结构、样式和交互。

数据流：发布表单 → JS FormData → POST /api/posts → Python 校验/图片处理 → SQLite → 返回详情地址。

## 测试

```bash
python -m pytest -q
```

Windows 虚拟环境可使用 `.venv\Scripts\python.exe -m pytest -q`。
测试使用独立临时数据库，不修改正常运行数据。

## 边界

这是课程作业的本地可运行版本，未增加账户登录、管理员审核、分页或线上部署。
“我的发布”依据签名 Cookie 内的随机身份，清除 Cookie、更换浏览器或删除 secret.key 后会失去原身份。
联系方式对访客可查看，折叠只是交互设计，不是访问权限控制。
服务器本地保存全部信息；正常重启不会丢失。备份时先停止服务，再复制 instance 文件夹。
不要将 instance（数据库、图片和密钥）提交到 Git。
默认不填充示例记录，可自行发布用于演示。未包含未提供的旧 App.tsx 源码，也未伪造原试用记录。
