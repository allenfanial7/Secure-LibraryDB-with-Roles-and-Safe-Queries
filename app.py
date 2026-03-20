from flask import Flask, render_template, request, jsonify, session
import sqlite3, os, datetime, hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)
DB = "library.db"

# ─────────────────────────────────────────
#  DATABASE INIT
# ─────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS book_info (
            book_id   INTEGER PRIMARY KEY,
            genre     TEXT,
            book_name TEXT,
            description TEXT,
            cover_emoji TEXT DEFAULT '📚'
        );

        CREATE TABLE IF NOT EXISTS student_info (
            student_name TEXT PRIMARY KEY,
            trade        TEXT,
            email        TEXT UNIQUE,
            mobile       TEXT,
            book_id      INTEGER,
            joined_at    TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(book_id) REFERENCES book_info(book_id)
        );

        CREATE TABLE IF NOT EXISTS reviews (
            review_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            book_id     INTEGER,
            rating      INTEGER CHECK(rating BETWEEN 1 AND 5),
            review_text TEXT,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(book_id) REFERENCES book_info(book_id)
        );

        CREATE TABLE IF NOT EXISTS roles (
            role_name   TEXT PRIMARY KEY,
            permissions TEXT,
            color       TEXT,
            icon        TEXT
        );

        CREATE TABLE IF NOT EXISTS users (
            username  TEXT PRIMARY KEY,
            role_name TEXT,
            password_hash TEXT,
            FOREIGN KEY(role_name) REFERENCES roles(role_name)
        );

        CREATE TABLE IF NOT EXISTS query_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            query_type TEXT,
            query_text TEXT,
            executed_at TEXT DEFAULT CURRENT_TIMESTAMP,
            success    INTEGER DEFAULT 1
        );
        """)

        # Seed books
        conn.executescript("""
        INSERT OR IGNORE INTO book_info VALUES
        (1,'Horror','The Shining','Haunted hotel, psychological fear','👻'),
        (2,'Horror','Dracula','Classic vampire horror','🧛'),
        (3,'Horror','The Haunting of Hill House','Ghosts + mental horror','🏚️'),
        (4,'Horror','Bird Box','Survival horror, unseen creatures','🙈'),
        (5,'Horror','It','Evil entity, childhood fear','🤡'),
        (6,'Comedy','The Hitchhiker''s Guide to the Galaxy','Sci-fi + comedy gold','🌌'),
        (7,'Comedy','Good Omens','Angels, demons & humor','😇'),
        (8,'Comedy','Bossypants','Funny life stories','😂'),
        (9,'Comedy','Three Men in a Boat','Classic British humor','🚣'),
        (10,'Comedy','Yes Please','Light, witty, inspiring','✨'),
        (11,'Fantasy','Harry Potter and the Philosopher''s Stone','Magic + friendship','⚡'),
        (12,'Fantasy','The Hobbit','Adventure in Middle-earth','💍'),
        (13,'Fantasy','A Game of Thrones','Politics + dragons','🐉'),
        (14,'Fantasy','Percy Jackson & the Lightning Thief','Mythology fantasy','⚡'),
        (15,'Fantasy','Mistborn: The Final Empire','Unique magic system','🌑'),
        (16,'Sci-Fi','Dune','Space politics + survival','🏜️'),
        (17,'Sci-Fi','1984','Dystopian future','👁️'),
        (18,'Sci-Fi','The Martian','Science + humor','🚀'),
        (19,'Sci-Fi','Fahrenheit 451','Book-burning future','🔥'),
        (20,'Sci-Fi','Ender''s Game','Space war strategy','🎮');
        """)

        # Seed roles (DCL concept)
        conn.executescript("""
        INSERT OR IGNORE INTO roles VALUES
        ('librarian_role',
         'ALL PRIVILEGES — SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, GRANT',
         '#d4a843', '👑');
        INSERT OR IGNORE INTO roles VALUES
        ('assistant_role',
         'SELECT, INSERT on StudentLibraryDB.*',
         '#7c9cbf', '📋');
        INSERT OR IGNORE INTO roles VALUES
        ('student_role',
         'SELECT on book_info only',
         '#7cbf8e', '🎓');
        """)

        # Seed sample users
        def h(p): return hashlib.sha256(p.encode()).hexdigest()
        conn.executescript(f"""
        INSERT OR IGNORE INTO users VALUES ('head_librarian','librarian_role','{h("lib123")}');
        INSERT OR IGNORE INTO users VALUES ('asst_librarian','assistant_role','{h("asst123")}');
        INSERT OR IGNORE INTO users VALUES ('student_user','student_role','{h("student123")}');
        """)
        conn.commit()

# ─────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/books")
def api_books():
    genre = request.args.get("genre","")
    with get_db() as conn:
        if genre:
            # PARAMETERIZED QUERY — safe from SQL injection
            q = "SELECT * FROM book_info WHERE genre = ?"
            rows = conn.execute(q, (genre,)).fetchall()
            _log(conn, "SELECT", q.replace("?", f"'{genre}'"))
        else:
            q = "SELECT * FROM book_info ORDER BY genre, book_id"
            rows = conn.execute(q).fetchall()
            _log(conn, "SELECT", q)
    return jsonify([dict(r) for r in rows])

@app.route("/api/register", methods=["POST"])
def api_register():
    d = request.json
    sql = "INSERT INTO student_info (student_name, trade, email, mobile, book_id) VALUES (?,?,?,?,?)"
    try:
        with get_db() as conn:
            # PARAMETERIZED — prevents SQL injection
            conn.execute(sql, (d["name"], d["trade"], d["email"], d["mobile"], d["book_id"]))
            conn.commit()
            _log(conn, "INSERT", sql)
        return jsonify({"ok": True, "message": f"Welcome, {d['name']}! 🎉"})
    except sqlite3.IntegrityError as e:
        return jsonify({"ok": False, "message": f"Error: {str(e)}"}), 409

@app.route("/api/students")
def api_students():
    with get_db() as conn:
        q = """SELECT s.student_name, s.trade, s.email, s.book_id,
                      b.book_name, b.genre, b.cover_emoji
               FROM student_info s
               JOIN book_info b ON s.book_id = b.book_id
               ORDER BY s.joined_at DESC"""
        rows = conn.execute(q).fetchall()
        _log(conn, "SELECT", q)
    return jsonify([dict(r) for r in rows])

@app.route("/api/reviews", methods=["GET","POST"])
def api_reviews():
    if request.method == "POST":
        d = request.json
        sql = "INSERT INTO reviews (student_name, book_id, rating, review_text) VALUES (?,?,?,?)"
        with get_db() as conn:
            conn.execute(sql, (d["student_name"], d["book_id"], d["rating"], d["review_text"]))
            conn.commit()
            _log(conn, "INSERT", sql)
        return jsonify({"ok": True})
    else:
        book_id = request.args.get("book_id")
        with get_db() as conn:
            if book_id:
                rows = conn.execute(
                    "SELECT r.*, b.book_name, b.cover_emoji FROM reviews r JOIN book_info b ON r.book_id=b.book_id WHERE r.book_id=? ORDER BY r.created_at DESC",
                    (book_id,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT r.*, b.book_name, b.cover_emoji FROM reviews r JOIN book_info b ON r.book_id=b.book_id ORDER BY r.created_at DESC LIMIT 20"
                ).fetchall()
        return jsonify([dict(r) for r in rows])

@app.route("/api/roles")
def api_roles():
    with get_db() as conn:
        roles = conn.execute("SELECT * FROM roles").fetchall()
        users = conn.execute("SELECT username, role_name FROM users").fetchall()
    return jsonify({
        "roles": [dict(r) for r in roles],
        "users": [dict(u) for u in users]
    })

@app.route("/api/query_log")
def api_query_log():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM query_log ORDER BY executed_at DESC LIMIT 15"
        ).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/stats")
def api_stats():
    with get_db() as conn:
        total_books    = conn.execute("SELECT COUNT(*) FROM book_info").fetchone()[0]
        total_students = conn.execute("SELECT COUNT(*) FROM student_info").fetchone()[0]
        total_reviews  = conn.execute("SELECT COUNT(*) FROM reviews").fetchone()[0]
        genres         = conn.execute("SELECT genre, COUNT(*) as cnt FROM book_info GROUP BY genre").fetchall()
    return jsonify({
        "total_books": total_books,
        "total_students": total_students,
        "total_reviews": total_reviews,
        "genres": [dict(g) for g in genres]
    })

def _log(conn, qtype, qtext):
    conn.execute(
        "INSERT INTO query_log (query_type, query_text) VALUES (?,?)",
        (qtype, qtext[:300])
    )
    conn.commit()

# ─────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
