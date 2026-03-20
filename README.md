# 📖 Secure LibraryDB v2.0
### Roles & Safe Queries — Flask Web Application

**Theme:** MySQL DCL (GRANT, REVOKE, CREATE USER, CREATE ROLE) + Python Parameterized Queries  
**Tools:** Flask · SQLite/MySQL · mysql-connector-python · HTML/CSS/JS  

---

## 🚀 Features

| Feature | Details |
|---|---|
| 📚 Book Library | 20 books across 4 genres with emoji covers |
| ✍️ Student Registration | Parameterized INSERT — SQL injection proof |
| ⭐ Live Reviews | Real-time book review system |
| 🔐 DCL Visualizer | GRANT, REVOKE, CREATE ROLE, CREATE USER |
| 🎓 Students Table | JOIN query with all registered students |
| 🛡️ Query Audit Log | Every query logged and displayed live |
| 📊 Permission Matrix | Role vs privilege visual table |

---

## ⚡ Quick Start (Local)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app (uses SQLite automatically)
python app.py

# 3. Open browser
http://localhost:5000
```

---

## 🌐 Deploy to Railway (Free Hosting)

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login & init
railway login
railway init

# 3. Deploy
railway up

# 4. Get your live URL
railway open
```

## 🌐 Deploy to Render (Free Hosting)

1. Push this folder to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set **Start Command:** `gunicorn app:app`
5. Deploy! ✅

---

## 🔐 DCL Concepts Demonstrated

```sql
-- ① Roles
CREATE ROLE librarian_role;
CREATE ROLE assistant_role;
CREATE ROLE student_role;

-- ② GRANT permissions to roles
GRANT ALL PRIVILEGES ON StudentLibraryDB.* TO librarian_role;
GRANT SELECT, INSERT  ON StudentLibraryDB.* TO assistant_role;
GRANT SELECT ON StudentLibraryDB.book_info  TO student_role;

-- ③ CREATE USER
CREATE USER 'student_user'@'localhost' IDENTIFIED BY 'Student@789';

-- ④ Assign role to user
GRANT student_role TO 'student_user'@'localhost';

-- ⑤ REVOKE
REVOKE INSERT ON StudentLibraryDB.book_info FROM assistant_role;
```

---

## 🛡️ SQL Injection Prevention

```python
# ❌ UNSAFE — never do this
sql = f"SELECT * FROM student_info WHERE name = '{user_input}'"

# ✅ SAFE — parameterized query
sql = "SELECT * FROM student_info WHERE name = %s"
cursor.execute(sql, (user_input,))
```

---

## 📁 Project Structure

```
SecureLibraryDB/
├── app.py                    # Flask backend (SQLite)
├── templates/
│   └── index.html            # Full frontend (Dark Academia theme)
├── Secure_LibraryDB_v2.sql   # MySQL production schema + DCL
├── requirements.txt
├── Procfile                  # For Railway/Render hosting
└── README.md
```

---

## 👑 Role Hierarchy

```
librarian_role  → ALL PRIVILEGES
    │
assistant_role  → SELECT + INSERT (no DELETE/DROP)
    │
student_role    → SELECT on book_info ONLY
```

---

*Built with Flask · SQLite · Dark Academia Design*
