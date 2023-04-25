CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    pwd TEXT,
    pfp TEXT,
    premium TEXT
);
CREATE TABLE IF NOT EXISTS gratitude(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    content TEXT,
    created DATE
);
CREATE TABLE IF NOT EXISTS moods(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    mood TEXT,
    note TEXT,
    diet TEXT,
    stress TEXT,
    exercise TEXT,
    created DATE
);