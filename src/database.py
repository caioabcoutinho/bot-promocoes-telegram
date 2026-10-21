import sqlite3
from src.config import DB_PATH
from src.stores import DEFAULT_STORES

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 10000")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def _add_column_if_missing(cursor, table, column, definition):
    columns = {row[1] for row in cursor.execute(f"PRAGMA table_info({table})")}
    if column not in columns:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def _migrate_promotion_url_constraint(cursor):
    unique_indexes = cursor.execute("PRAGMA index_list(promotions)").fetchall()
    has_url_only_unique_index = False
    for index in unique_indexes:
        if not index[2]:
            continue
        columns = [
            row[2] for row in cursor.execute(f"PRAGMA index_info({index[1]})")
        ]
        if columns == ["url"]:
            has_url_only_unique_index = True
            break
    if not has_url_only_unique_index:
        return
    cursor.execute("PRAGMA foreign_keys = OFF")
    cursor.execute(
        """CREATE TABLE promotions_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price REAL,
            store TEXT,
            url TEXT,
            coupon TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            chat_id INTEGER,
            message_id INTEGER,
            source_channel TEXT,
            notified_at DATETIME,
            notification_error TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id),
            UNIQUE(product_id, url)
        )"""
    )
    cursor.execute(
        """INSERT INTO promotions_v2
           (id, product_id, price, store, url, coupon, timestamp,
            chat_id, message_id, notified_at, notification_error)
           SELECT id, product_id, price, store, url, coupon, timestamp,
                  chat_id, message_id, notified_at, notification_error
           FROM promotions"""
    )
    cursor.execute("DROP TABLE promotions")
    cursor.execute("ALTER TABLE promotions_v2 RENAME TO promotions")


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, keywords TEXT, exclude_words TEXT, target_price REAL, max_price REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS raw_matches (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, channel TEXT, message_text TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(product_id) REFERENCES products(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS promotions (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, price REAL, store TEXT, url TEXT UNIQUE, coupon TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(product_id) REFERENCES products(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS stores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        aliases TEXT NOT NULL DEFAULT '',
        domains TEXT NOT NULL DEFAULT '',
        blocked INTEGER NOT NULL DEFAULT 0
    )''')
    _add_column_if_missing(cursor, "raw_matches", "message_id", "INTEGER")
    _add_column_if_missing(cursor, "raw_matches", "chat_id", "INTEGER")
    _add_column_if_missing(cursor, "promotions", "chat_id", "INTEGER")
    _add_column_if_missing(cursor, "promotions", "message_id", "INTEGER")
    _add_column_if_missing(cursor, "promotions", "source_channel", "TEXT")
    _add_column_if_missing(cursor, "promotions", "notified_at", "DATETIME")
    _add_column_if_missing(cursor, "promotions", "notification_error", "TEXT")
    _migrate_promotion_url_constraint(cursor)
    for name, aliases, domains in DEFAULT_STORES:
        cursor.execute(
            """INSERT OR IGNORE INTO stores (name, aliases, domains, blocked)
               VALUES (?, ?, ?, 0)""",
            (name, ",".join(aliases), ",".join(domains)),
        )
    conn.commit()
    conn.close()

def add_product(name, keywords, exclude_words, target_price, max_price):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO products (name, keywords, exclude_words, target_price, max_price) VALUES (?, ?, ?, ?, ?)', (name, keywords, exclude_words, target_price, max_price))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_product(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE name = ?', (name,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, keywords, exclude_words, target_price FROM products')
    rows = cursor.fetchall()
    conn.close()
    products = []
    for r in rows:
        products.append({'id': r[0], 'name': r[1], 'keywords': r[2].split(',') if r[2] else [], 'exclude_words': r[3].split(',') if r[3] else [], 'target_price': r[4]})
    return products

def update_target_price(name, new_price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE products SET target_price = ? WHERE name = ?', (new_price, name))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated

def save_raw_match(product_id, channel, message_text, chat_id=None, message_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO raw_matches
           (product_id, channel, message_text, chat_id, message_id)
           VALUES (?, ?, ?, ?, ?)""",
        (product_id, channel, message_text, chat_id, message_id),
    )
    conn.commit()
    conn.close()


def add_store(name, aliases="", domains="", blocked=False):
    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO stores (name, aliases, domains, blocked)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(name) DO UPDATE SET
                 aliases=excluded.aliases,
                 domains=excluded.domains,
                 blocked=excluded.blocked""",
            (name.strip(), aliases, domains, int(blocked)),
        )
        conn.commit()
    finally:
        conn.close()


def delete_store(name):
    conn = get_connection()
    try:
        cursor = conn.execute("DELETE FROM stores WHERE name = ?", (name,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def set_store_blocked(name, blocked):
    conn = get_connection()
    try:
        cursor = conn.execute(
            "UPDATE stores SET blocked = ? WHERE name = ?", (int(blocked), name)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def get_stores():
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT name, aliases, domains, blocked FROM stores ORDER BY name"
        ).fetchall()
        return [
            (
                row["name"],
                [value.strip() for value in row["aliases"].split(",") if value.strip()],
                [value.strip().casefold() for value in row["domains"].split(",") if value.strip()],
                bool(row["blocked"]),
            )
            for row in rows
        ]
    finally:
        conn.close()

def save_promotion(
    product_id,
    price,
    store,
    url,
    coupon=None,
    chat_id=None,
    message_id=None,
    source_channel=None,
):
    conn = get_connection()
    cursor = conn.cursor()
    saved = False
    try:
        cursor.execute(
            """INSERT INTO promotions
               (product_id, price, store, url, coupon, chat_id, message_id,
                source_channel)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (product_id, price, store, url, coupon, chat_id, message_id,
             source_channel),
        )
        conn.commit()
        saved = True
    except sqlite3.IntegrityError:
        cursor.execute(
            """UPDATE promotions
               SET price = ?, store = ?, coupon = ?, timestamp = CURRENT_TIMESTAMP,
                   chat_id = ?, message_id = ?, source_channel = ?,
                   notification_error = NULL
               WHERE product_id = ? AND url = ?""",
            (
                price,
                store,
                coupon,
                chat_id,
                message_id,
                source_channel,
                product_id,
                url,
            ),
        )
        conn.commit()
        saved = cursor.rowcount > 0
    finally:
        conn.close()
    return saved


def is_recent_duplicate(product_id, price, url, minutes=30):
    conn = get_connection()
    try:
        row = conn.execute(
            """SELECT 1 FROM promotions
               WHERE product_id = ? AND price = ? AND url = ?
                 AND timestamp >= datetime('now', ?) LIMIT 1""",
            (product_id, price, url, f"-{int(minutes)} minutes"),
        ).fetchone()
        return row is not None
    finally:
        conn.close()

def get_recent_promotions(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT prom.id, prod.name, prom.price, prom.store, prom.url, prom.coupon,
        prom.timestamp, prom.chat_id, prom.message_id, prom.source_channel,
        prom.notified_at,
        prom.notification_error
        FROM promotions prom JOIN products prod ON prom.product_id = prod.id
        ORDER BY prom.timestamp DESC LIMIT ?''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_promotion(promotion_id):
    conn = get_connection()
    try:
        return conn.execute(
            """SELECT prom.id, prod.name, prom.price, prom.store, prom.url,
                      prom.coupon, prom.source_channel
               FROM promotions prom
               JOIN products prod ON prod.id = prom.product_id
               WHERE prom.id = ?""",
            (promotion_id,),
        ).fetchone()
    finally:
        conn.close()


def record_notification_by_id(promotion_id, success, error=None):
    conn = get_connection()
    try:
        conn.execute(
            """UPDATE promotions
               SET notified_at = CASE WHEN ? THEN CURRENT_TIMESTAMP ELSE notified_at END,
                   notification_error = ?
               WHERE id = ?""",
            (int(success), error, promotion_id),
        )
        conn.commit()
    finally:
        conn.close()


def record_notification(product_id, url, success, error=None):
    conn = get_connection()
    try:
        conn.execute(
            """UPDATE promotions
               SET notified_at = CASE WHEN ? THEN CURRENT_TIMESTAMP ELSE notified_at END,
                   notification_error = ?
               WHERE product_id = ? AND url = ?""",
            (int(success), error, product_id, url),
        )
        conn.commit()
    finally:
        conn.close()


def get_statistics():
    conn = get_connection()
    try:
        return {
            "products": conn.execute("SELECT COUNT(*) FROM products").fetchone()[0],
            "stores": conn.execute("SELECT COUNT(*) FROM stores").fetchone()[0],
            "blocked_stores": conn.execute(
                "SELECT COUNT(*) FROM stores WHERE blocked = 1"
            ).fetchone()[0],
            "promotions": conn.execute("SELECT COUNT(*) FROM promotions").fetchone()[0],
            "matches": conn.execute("SELECT COUNT(*) FROM raw_matches").fetchone()[0],
        }
    finally:
        conn.close()
