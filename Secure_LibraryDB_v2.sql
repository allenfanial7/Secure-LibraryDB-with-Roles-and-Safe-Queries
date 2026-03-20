-- ═══════════════════════════════════════════
--  Secure LibraryDB v2.0 — Full Schema
--  Theme: MySQL DCL + Parameterized Queries
-- ═══════════════════════════════════════════

CREATE DATABASE IF NOT EXISTS StudentLibraryDB;
USE StudentLibraryDB;

-- ── TABLES ──────────────────────────────────

CREATE TABLE IF NOT EXISTS book_info (
    book_id     INT PRIMARY KEY,
    genre       VARCHAR(20)  NOT NULL,
    book_name   VARCHAR(100) NOT NULL,
    description VARCHAR(200),
    cover_emoji VARCHAR(10) DEFAULT '📚'
);

CREATE TABLE IF NOT EXISTS student_info (
    student_name VARCHAR(50)  PRIMARY KEY,
    trade        VARCHAR(30),
    email        VARCHAR(50)  UNIQUE,
    mobile       VARCHAR(15),
    book_id      INT,
    joined_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES book_info(book_id)
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id    INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(50),
    book_id      INT,
    rating       TINYINT CHECK (rating BETWEEN 1 AND 5),
    review_text  TEXT,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES book_info(book_id)
);

CREATE TABLE IF NOT EXISTS query_log (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    query_type  VARCHAR(10),
    query_text  TEXT,
    executed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    success     TINYINT DEFAULT 1
);

-- ── SEED BOOKS ───────────────────────────────

INSERT IGNORE INTO book_info VALUES
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


-- ═══════════════════════════════════════════
--  DCL SECTION — Data Control Language
-- ═══════════════════════════════════════════

-- ① Drop existing roles/users (clean slate)
DROP ROLE IF EXISTS librarian_role, assistant_role, student_role;
DROP USER IF EXISTS
    'head_librarian'@'localhost',
    'asst_librarian'@'localhost',
    'student_user'@'localhost';

-- ② Create Roles
CREATE ROLE librarian_role;
CREATE ROLE assistant_role;
CREATE ROLE student_role;

-- ③ Grant Permissions to Roles
GRANT ALL PRIVILEGES ON StudentLibraryDB.*      TO librarian_role;
GRANT SELECT, INSERT  ON StudentLibraryDB.*      TO assistant_role;
GRANT SELECT          ON StudentLibraryDB.book_info TO student_role;

-- ④ Create Database Users
CREATE USER 'head_librarian'@'localhost' IDENTIFIED BY 'Lib@Secure123';
CREATE USER 'asst_librarian'@'localhost' IDENTIFIED BY 'Asst@Secure456';
CREATE USER 'student_user'@'localhost'   IDENTIFIED BY 'Student@789';

-- ⑤ Assign Roles to Users
GRANT librarian_role TO 'head_librarian'@'localhost';
GRANT assistant_role  TO 'asst_librarian'@'localhost';
GRANT student_role    TO 'student_user'@'localhost';

-- ⑥ Revoke DELETE from assistant (example REVOKE)
REVOKE INSERT ON StudentLibraryDB.book_info FROM assistant_role;

FLUSH PRIVILEGES;
