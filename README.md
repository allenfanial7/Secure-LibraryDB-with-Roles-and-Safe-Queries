# 📖 Secure LibraryDB with Roles and Safe Queries

## 🧠 About This Project

This is a simple library management project made using Python (Flask) and database concepts.

In this project, I tried to understand:

* How database security works
* How roles and permissions are used (DCL)
* How to prevent SQL Injection using safe queries

This project is mainly for learning purposes.

---

## 🚀 Features

* 📚 Shows different books by category
* ✍️ Student registration form
* ⭐ Students can give reviews to books
* 🔐 Different roles (Librarian, Assistant, Student)
* 🛡️ Safe database queries (no SQL injection)
* 📊 Shows query logs (what is happening in database)

---

## 🛠️ Technologies Used

* Python (Flask)
* SQLite / MySQL
* HTML, CSS, JavaScript

---

## ▶️ How to Run This Project

Follow these simple steps:

### Step 1: Install requirements

```
pip install -r requirements.txt
```

### Step 2: Run the project

```
python app.py
```

### Step 3: Open browser

```
http://localhost:5000
```

---

## 🔐 What I Learned

* What is DCL (Data Control Language)
* How to use:

  * GRANT
  * REVOKE
  * CREATE USER
  * CREATE ROLE
* How to use parameterized queries in Python
* How to connect frontend with backend

---

## 🛡️ SQL Injection Example

❌ Wrong way:

```
sql = "SELECT * FROM users WHERE name = '" + user_input + "'"
```

✅ Correct way:

```
sql = "SELECT * FROM users WHERE name = %s"
cursor.execute(sql, (user_input,))
```

---

## 📁 Project Structure

```
SecureLibraryDB/
│── app.py
│── library.db
│── requirements.txt
│── README.md
│── templates/
│    └── index.html
```

---

## 👥 Roles in This Project

* 👑 Librarian → Full access
* 📋 Assistant → Can read and add data
* 🎓 Student → Can only view books

---

## 📌 Note

This project is made for learning database security and backend concepts.
It is not a production-level system.

---

## 🧏🏻 Author

Made by ALLEN FANIAL while learning Flask and Database 🙂
