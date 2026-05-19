import sqlite3


DB_NAME = "translations.db"


# CREATE DATABASE TABLE
def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS translations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT,

            original_text TEXT,

            translated_text TEXT,

            detected_language TEXT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    conn.close()


# SAVE TRANSLATION
def save_translation(
    user_id,
    original_text,
    translated_text,
    detected_language
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO translations (
            user_id,
            original_text,
            translated_text,
            detected_language
        )

        VALUES (?, ?, ?, ?)
    """, (
        str(user_id),
        original_text,
        translated_text,
        detected_language
    ))

    conn.commit()

    conn.close()


# FETCH USER HISTORY
def get_user_history(user_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            original_text,
            translated_text,
            detected_language,
            timestamp

        FROM translations

        WHERE user_id = ?

        ORDER BY id DESC

        LIMIT 5
    """, (str(user_id),))

    history = cursor.fetchall()

    conn.close()

    return history