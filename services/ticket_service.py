from database import get_connection, update_ticket_status
import random


def generate_ticket_id():
    """
    Generate a unique support ticket ID.
    """
    return f"TKT{random.randint(100000, 999999)}"


def create_ticket(name, email, subject, message):
    """
    Create a new support ticket.
    """

    ticket_id = generate_ticket_id()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tickets (
            ticket_id,
            name,
            email,
            subject,
            message,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        ticket_id,
        name,
        email,
        subject,
        message,
        "Open"
    ))

    connection.commit()
    connection.close()

    return ticket_id


def get_all_tickets():
    """
    Return all support tickets.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM tickets
        ORDER BY id DESC
    """)

    tickets = cursor.fetchall()

    connection.close()

    return tickets


def get_open_tickets():
    """
    Return only open support tickets.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM tickets
        WHERE status = 'Open'
        ORDER BY id DESC
    """)

    tickets = cursor.fetchall()

    connection.close()

    return tickets


def close_ticket(ticket_id):
    """
    Close a support ticket.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tickets
        SET status = 'Closed'
        WHERE ticket_id = ?
    """, (ticket_id,))

    connection.commit()
    connection.close()

def change_ticket_status(ticket_id, status):
    """
    Change the status of a ticket.
    """
    update_ticket_status(ticket_id, status)