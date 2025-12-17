# mini-login（SQLi + XSS 修補導向）

## 0. 修改學號
請打開 `docker-compose.yml`，把：
- `container_name: mini_login_B11234567`
- `OWNER=B11234567`

改成你自己的學號。

## 1. 啟動
```bash
docker compose up -d --build
```

## 2. 上線檢查（必做）
打開：
- http://你的IP:5000/health

要看到類似：
```json
{"ok":true,"owner":"B11234567","version":"vuln"}
```

## 3. SQL Injection：修補前 PoC（先證明漏洞存在）
```bash
curl -i -X POST http://你的IP:5000/login \
  -d "username=' OR '1'='1" -d "password=x"
```
修補前應回 `HTTP/1.1 200 OK`

## 4. SQL Injection：修補
打開 `app.py`，找到 `/login` 裡面標示 TODO 的區塊，把字串拼接 SQL 改成「參數化查詢」：
- SQL: `SELECT role FROM users WHERE username=? AND password=?`
- 使用 `q_one_params(sql, (username, password))`

修補後用相同 payload 再打一次，應回 `401 Unauthorized`

## 5. XSS：修補前 PoC
打開：
- http://你的IP:5000/comment

輸入：
```html
<script>alert('XSS')</script>
```
修補前應會跳出 alert。

## 6. XSS：修補
在 `app.py` 的 `/comment` 迴圈輸出位置，把：
```python
page += f"<li>{c}</li>"
```
改成：
```python
safe = html.escape(c)
page += f"<li>{safe}</li>"
```

修補後再輸入一次 payload，不得跳 alert，頁面只顯示文字。

## 7. 讓修補生效（重建）
```bash
docker compose down
docker compose up -d --build
```
