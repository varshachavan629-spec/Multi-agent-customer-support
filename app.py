from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect
)
from flask import Flask, render_template, request, jsonify, session
from services.ticket_service import (
    create_ticket,
    get_all_tickets,
    change_ticket_status
)
from config import Config
from database import create_user
import uuid

from database import (
    create_tables,
    get_all_conversations,
    get_total_conversations,
    get_agent_count,
    get_recent_conversations,
    verify_admin,
    verify_user,
    get_ticket_count,
    get_user_tickets
)
from services.chat_service import process_chat
from services.ticket_service import create_ticket

app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Required for Flask Session
app.secret_key = Config.SECRET_KEY

# Create database tables when the application starts
create_tables()

# ---------------- Login ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        role = request.form.get("role")
        username = request.form.get("username")
        password = request.form.get("password")

        # ---------------- Admin Login ----------------
        if role == "admin":

            admin = verify_admin(username, password)

            if admin:
                session["role"] = "admin"
                session["username"] = username
                return redirect("/dashboard")

        # ---------------- User Login ----------------
        elif role == "user":

            email = username

            print("Role:", role)
            print("Email:", email)
            print("Password:", password)

            user = verify_user(email, password)

            print("User Found:", user)

            if user:
                session["role"] = "user"
                session["username"] = user[2]   # Email
                session["name"] = user[1]       # Name

                return redirect("/")

        return render_template(
            "login.html",
            error="Invalid Username or Password."
        )

    return render_template("login.html")


# ---------------- Register ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            create_user(name, email, password)

            print("✅ User registered successfully")

            return redirect("/login")

        except Exception as e:

            print("Registration Error:", e)

            return render_template(
                "register.html",
                error=str(e)
            )

    return render_template("register.html")
# ---------------- Home ----------------
@app.route("/")
def home():
# Not logged in → Login page
    if "role" not in session:
        return redirect("/login")

    # Admin → Dashboard
    if session["role"] == "admin":
        return redirect("/dashboard")

    # User → Home page
    return render_template("index.html")

# ---------------- Chat ----------------
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if session.get("role") != "user":
     return redirect("/login")

    if request.method == "POST":

        # Create a session ID for each user
        if "session_id" not in session:
            session["session_id"] = str(uuid.uuid4())

        session_id = session["session_id"]

        data = request.get_json()

        user_message = data.get("message")

        result = process_chat(
            user_message=user_message,
            session_id=session_id
        )

        return jsonify(result)

    return render_template("chat.html")


# ---------------- Dashboard ----------------
@app.route("/dashboard")
def dashboard():
    recent = get_recent_conversations()
    open_tickets = get_ticket_count("Open")
    in_progress = get_ticket_count("In Progress")
    resolved = get_ticket_count("Resolved")


    # Allow only admins
    if session.get("role") != "admin":
        return redirect("/login")

    total = get_total_conversations()

    billing = get_agent_count("Billing")

    technical = get_agent_count("Technical")

    account = get_agent_count("Account")

    general = get_agent_count("General")

    escalation = get_agent_count("Escalation")

  
    return render_template(
    "dashboard.html",
    total=total,
    billing=billing,
    technical=technical,
    account=account,
    general=general,
    escalation=escalation,
    recent=recent,
    open_tickets=open_tickets,
    in_progress=in_progress,
    resolved=resolved
)
# ---------------- History ----------------
@app.route("/history")
def history():

    # Allow only admins
    if session.get("role") != "admin":
        return redirect("/login")

    conversations = get_all_conversations()

    return render_template(
        "history.html",
        conversations=conversations
    )


# ---------------- About ----------------
@app.route("/about")
def about():
    if session.get("role") != "user":
     return redirect("/login")

    return render_template("about.html")
    

# ---------------- Contact ----------------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if session.get("role") != "user":
     return redirect("/login")


    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        ticket_id = create_ticket(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        return render_template(
            "ticket_success.html",
            ticket=ticket_id
        )

    return render_template("contact.html")


@app.route("/my-tickets")
def my_tickets():

    if session.get("role") != "user":
        return redirect("/login")

    email = session["username"]

    # Get ticket ID from search box
    ticket_id = request.args.get("ticket_id")

    tickets = get_user_tickets(email, ticket_id)

    return render_template(
        "my_tickets.html",
        tickets=tickets,
        ticket_id=ticket_id
    )


@app.route("/tickets")
def tickets():

    # Allow only admins
    if session.get("role") != "admin":
        return redirect("/login")

    tickets = get_all_tickets()

    return render_template(
        "tickets.html",
        tickets=tickets
    )


@app.route("/ticket/update/<ticket_id>", methods=["POST"])
def update_ticket(ticket_id):

    if session.get("role") != "admin":
        return redirect("/login")

    status = request.form.get("status")

    change_ticket_status(ticket_id, status)

    return redirect("/tickets")


# ---------------- Error ----------------
@app.route("/error")
def error():
    return render_template("error.html")


# ---------------- Logout ----------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)