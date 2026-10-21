import sqlite3

import src.database as database


def test_init_db_migrates_url_uniqueness_and_preserves_data(tmp_path, monkeypatch):
    db_path = tmp_path / "monitor.db"
    monkeypatch.setattr(database, "DB_PATH", str(db_path))
    conn = sqlite3.connect(db_path)
    conn.executescript(
        """CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE,
            keywords TEXT, exclude_words TEXT, target_price REAL, max_price REAL
        );
        CREATE TABLE raw_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER,
            channel TEXT, message_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE promotions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER,
            price REAL, store TEXT, url TEXT UNIQUE, coupon TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        INSERT INTO products VALUES (1, 'GPU', 'gpu', '', 1000, 1200);
        INSERT INTO promotions (product_id, price, store, url, coupon)
        VALUES (1, 900, 'KaBuM!', 'https://kabum.com.br/gpu', 'GPU10');
        """
    )
    conn.commit()
    conn.close()

    database.init_db()
    conn = sqlite3.connect(db_path)
    assert conn.execute("SELECT count(*) FROM products").fetchone()[0] == 1
    assert conn.execute("SELECT count(*) FROM promotions").fetchone()[0] == 1
    indexes = conn.execute("PRAGMA index_list(promotions)").fetchall()
    assert any(row[2] for row in indexes)
    conn.close()
