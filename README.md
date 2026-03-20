# 📖 Secure LibraryDB with Roles and Safe Queries

## 🔐 Project Overview

This project is a secure Library Management System built using **Flask + SQLite/MySQL** that demonstrates:

* ✅ MySQL DCL (GRANT, REVOKE, CREATE USER, ROLE)
* ✅ Role-Based Access Control (RBAC)
* ✅ SQL Injection Prevention using Parameterized Queries
* ✅ Query Logging System
* ✅ Interactive Web UI

---

## 🚀 Features

* 📚 Book Library (20+ books with categories)
* ✍️ Student Registration (Safe INSERT queries)
* ⭐ Book Review System
* 🔐 Role-Based Access (Librarian, Assistant, Student)
* 🛡️ SQL Injection Protection
* 📊 Query Audit Log
* 📈 Permission Matrix Visualization

---

## 🛠️ Technologies Used

* Python (Flask)
* SQLite / MySQL
* mysql-connector-python
* HTML, CSS, JavaScript

---

## ⚡ How to Run (Step-by-Step)

### 1️⃣ Install Requirements

```
pip install -r requirements.txt
```

### 2️⃣ Run the Project

```
python app.py
```

### 3️⃣ Open in Browser

```
http://localhost:5000
```

---

## 🔐 DCL Concepts Used

```sql
CREATE ROLE librarian_role;
CREATE ROLE assistant_role;
CREATE ROLE student_role;

GRANT ALL PRIVILEGES ON StudentLibraryDB.* TO librarian_role;
GRANT SELECT, INSERT ON StudentLibraryDB.* TO assistant_role;
GRANT SELECT ON StudentLibraryDB.book_info TO student_role;

CREATE USER 'student_user'@'localhost' IDENTIFIED BY 'password';

GRANT student_role TO 'student_user'@'localhost';

REVOKE INSERT ON StudentLibraryDB.book_info FROM assistant_role;
```

---

## 🛡️ SQL Injection Protection

❌ Unsafe Query:

```python
sql = f"SELECT * FROM student WHERE name = '{user_input}'"
```

✅ Safe Query:

```python
sql = "SELECT * FROM student WHERE name = %s"
cursor.execute(sql, (user_input,))
```

---

## 📁 Project Structure

```
SecureLibraryDB/
│── app.py
│── library.db
│── Secure_LibraryDB_v2.sql
│── requirements.txt
│── Procfile
│── templates/
│    └── index.html
│── README.md
```

---

## 👥 Roles

| Role         | Permissions   |
| ------------ | ------------- |
| 👑 Librarian | Full Access   |
| 📋 Assistant | Read + Insert |
| 🎓 Student   | Read Only     |

---

## 💡 Learning Outcome

* Understanding of Database Security
* Practical use of DCL commands
* Prevention of SQL Injection
* Backend + Database Integration

---

## 📌 Author

Made with ❤️ using Flask & MySQL
