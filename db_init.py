import sqlite3

DB = "users.db"

def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users;")
    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        );
    """)
    # Demo accounts
    cur.execute("INSERT INTO users(username,password,role) VALUES ('admin','admin123','admin');")
    cur.execute("INSERT INTO users(username,password,role) VALUES ('student','pass123','user');")
    conn.commit()
    conn.close()
    print("DB initialized:", DB)

if __name__ == "__main__":
    main()
