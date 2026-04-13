"""Handle user operations."""

import sqlite3


def get_user(user_id):
    """Fetch a user from the database."""
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # WARNING: This has a SQL injection vulnerability (Claude will catch this)
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    return result


def create_user(name, email):
    """Create a new user."""
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO users (name, email) VALUES ('{name}', '{email}')"
    )
    conn.commit()
    # Connection is never closed (Claude will catch this too)
    return True


def delete_all_users():
    """Delete every user from the database."""
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    return True
