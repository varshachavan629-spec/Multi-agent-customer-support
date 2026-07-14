import sqlite3
from config import Config


def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    return sqlite3.connect(Config.DATABASE)


def create_tables():
    """
    Creates the conversations and tickets tables.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # Conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            session_id TEXT NOT NULL,

            user_message TEXT NOT NULL,

            agent TEXT NOT NULL,

            bot_response TEXT NOT NULL,

            status TEXT NOT NULL,

            timestamp TEXT NOT NULL

        )
    """)

    # Tickets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            ticket_id TEXT NOT NULL,

            name TEXT NOT NULL,

            email TEXT NOT NULL,

            subject TEXT NOT NULL,

            message TEXT NOT NULL,

            status TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # ---------------- Users Table ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)

    # ---------------- Admin Table ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)

    # Default Admin
    cursor.execute("""
        INSERT OR IGNORE INTO admins (
            id,
            username,
            password
        )
        VALUES (?, ?, ?)
    """, (
        1,
        "admin",
        "admin123"
    ))

    connection.commit()
    connection.close()

    print("✅ Database tables created successfully!")


def save_conversation(
    session_id,
    user_message,
    agent,
    bot_response,
    status,
    timestamp
):
    """
    Save a conversation into the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO conversations (
            session_id,
            user_message,
            agent,
            bot_response,
            status,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        session_id,
        user_message,
        agent,
        bot_response,
        status,
        timestamp
    ))

    connection.commit()
    connection.close()

    print("✅ Conversation saved successfully!")


def get_all_conversations():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM conversations
        ORDER BY id DESC
    """)

    conversations = cursor.fetchall()

    connection.close()

    return conversations


def get_conversation_by_id(conversation_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM conversations
        WHERE id=?
    """, (conversation_id,))

    conversation = cursor.fetchone()

    connection.close()

    return conversation


def delete_conversation(conversation_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM conversations
        WHERE id=?
    """, (conversation_id,))

    connection.commit()
    connection.close()

    print("✅ Conversation deleted successfully!")


def get_total_conversations():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM conversations
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_agent_count(agent_name):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM conversations
        WHERE agent=?
    """, (agent_name,))

    count = cursor.fetchone()[0]

    connection.close()

    return count


def get_recent_conversations(limit=5):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            user_message,
            agent,
            timestamp
        FROM conversations
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    conversations = cursor.fetchall()

    connection.close()

    return conversations


def get_last_conversations(session_id, limit=5):
    """
    Returns only previous user messages for the current session.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT user_message
        FROM conversations
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (session_id, limit))

    conversations = cursor.fetchall()

    connection.close()

    return conversations[::-1]

def verify_admin(username, password):
    """
    Verify admin login credentials.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM admins
        WHERE username = ?
        AND password = ?
    """, (username, password))

    admin = cursor.fetchone()

    connection.close()

    return admin

def verify_user(email, password):
    """
    Verify user login credentials.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email = ?
        AND password = ?
    """, (email, password))

    user = cursor.fetchone()

    connection.close()

    return user

def create_user(name, email, password):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users(name, email, password)
            VALUES (?, ?, ?)
        """, (name, email, password))

        connection.commit()

    finally:
        connection.close()
        
def update_ticket_status(ticket_id, status):
    """
    Update ticket status.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tickets
        SET status = ?
        WHERE ticket_id = ?
    """, (status, ticket_id))

    connection.commit()
    connection.close()

    print("✅ Ticket status updated!")

def get_ticket_count(status):
    """
    Returns the number of tickets for a given status.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tickets
        WHERE status = ?
    """, (status,))

    count = cursor.fetchone()[0]

    connection.close()

    return count

def get_user_tickets(email, ticket_id=None):
    """
    Returns tickets of the logged-in user.
    If ticket_id is provided, returns only that ticket.
    """

    connection = get_connection()
    cursor = connection.cursor()

    if ticket_id:

        cursor.execute("""
            SELECT *
            FROM tickets
            WHERE email = ?
            AND ticket_id = ?
            ORDER BY id DESC
        """, (email, ticket_id))

    else:

        cursor.execute("""
            SELECT *
            FROM tickets
            WHERE email = ?
            ORDER BY id DESC
        """, (email,))

    tickets = cursor.fetchall()

    connection.close()

    return tickets