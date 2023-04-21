CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    pin TEXT,
    pfp TEXT,
    premium INTEGER,
    joined DATE,
)
CREATE TABLE gratitude(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    content TEXT,
    created DATE
)
CREATE TABLE moods(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    mood TEXT,
    note TEXT,
    diet TEXT,
    stress TEXT,
    exercise TEXT,
    created DATE,
    note TEXT
)