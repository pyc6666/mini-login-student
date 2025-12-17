import os
import sqlite3
import html
from flask import Flask, request, jsonify

APP = Flask(__name__)
OWNER = os.getenv("OWNER", "UNKNOWN")
MODE = os.getenv("MODE", "vuln")  # vuln / patched（僅顯示用）
DB = "users.db"

# in-memory comments (demo)
COMMENTS = []

def q_one(sql: str):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchone()
    conn.close()
    return row

def q_one_params(sql: str, params: tuple):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(sql, params)
    row = cur.fetchone()
    conn.close()
    return row

@APP.get("/health")
def health():
    return jsonify({
        "ok": True,
        "owner": OWNER,
        "version": MODE
    }), 200

@APP.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return (
            "<h2>Login</h2>"
            "<form method='POST'>"
            "Username: <input name='username'><br>"
            "Password: <input name='password' type='password'><br><br>"
            "<button type='submit'>Login</button>"
            "</form>"
            "<p><a href='/'>Back</a></p>"
        )

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # ==========================================================
    # SQL Injection（脆弱版）
    # TODO(學生修補)：改成參數化查詢（Prepared / Parameterized）
    # 目標：payload username="' OR '1'='1" 不得再登入成功（應回 401）
    # ==========================================================
    sql = (
        "SELECT role FROM users "
        f"WHERE username='{username}' AND password='{password}'"
    )
    row = q_one(sql)

    if row:
        return jsonify({"login": "ok", "owner": OWNER, "role": row[0]}), 200
    return jsonify({"login": "fail", "owner": OWNER}), 401

@APP.route("/comment", methods=["GET", "POST"])
def comment():
    # ==========================================================
    # XSS（脆弱版）
    # TODO(學生修補)：輸出前做 html.escape，避免 <script> 被執行
    # 目標：payload <script>alert('XSS')</script> 不得觸發 alert
    # ==========================================================
    if request.method == "POST":
        text = request.form.get("text", "")
        COMMENTS.append(text)

    page = "<h2>Comments</h2><ul>"
    for c in COMMENTS:
        # 脆弱：未編碼直接輸出
        page += f"<li>{c}</li>"
    page += "</ul>"

    page += (
        "<form method='POST'>"
        "<input name='text' style='width: 360px'>"
        "<button type='submit'>Submit</button>"
        "</form>"
        "<p><a href='/'>Back</a></p>"
    )
    return page

@APP.get("/")
def index():
    # 簡單首頁（含 owner）
    return (
        "<h2>mini-login</h2>"
        f"<p id='owner'>Server Owner: {OWNER}</p>"
        "<ul>"
        "<li>Login: <a href='/login'>/login</a></li>"
        "<li>Comment: <a href='/comment'>/comment</a></li>"
        "<li>Health: <a href='/health'>/health</a></li>"
        "</ul>"
    )

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5000, debug=False)
