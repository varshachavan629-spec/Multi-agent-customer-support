
# 🤖 MultiAgent AI Customer Support

MultiAgent AI Customer Support is an AI-powered customer support system built using **Python**, **Flask**, **LangChain**, **LangGraph**, **Groq LLM**, and **SQLite**. The application intelligently routes customer queries to specialized AI agents, retrieves answers from a CSV-based knowledge base, falls back to the Groq LLM when needed, stores conversation history, and provides a complete support ticket management system with separate User and Admin portals.

---

# 🚀 Features

## 👤 User Features

- User Registration & Login
- AI Chat Support
- Multi-Agent Query Routing
- CSV-based Knowledge Base
- Intelligent Fallback to Groq LLM
- Conversation History
- Contact Support Form
- Support Ticket Generation
- View My Tickets
- Search Tickets by Ticket ID
- Track Ticket Status (Open, In Progress, Resolved)
- Logout

---

## 👨‍💼 Admin Features

- Secure Admin Login
- Dashboard Analytics
- View Conversation History
- View All Support Tickets
- Update Ticket Status
  - Open
  - In Progress
  - Resolved
- Monitor Customer Queries
- Logout

---

# 🤖 Multi-Agent Architecture

The application automatically routes every customer query to the most suitable AI agent.

### 💳 Billing Agent
Handles:
- Payment Issues
- Refund Requests
- Billing Queries
- Subscription Queries

### 🔧 Technical Agent
Handles:
- Software Errors
- Login Problems
- Application Crashes
- Technical Troubleshooting

### 👤 Account Agent
Handles:
- Password Reset
- Username Recovery
- Account Management
- Profile-related Queries

### ❓ General Agent
Handles:
- General Questions
- Product Information
- Frequently Asked Questions

### 🚨 Escalation Agent
Handles:
- Complex Issues
- Unresolved Customer Problems
- Human Support Escalation

---

# 📚 Knowledge Base

The application uses **CSV files** as a lightweight knowledge base for different customer support domains.

Available knowledge files:

- billing.csv
- technical.csv
- account.csv
- general.csv

### Response Generation Process

1. The Triaging Agent identifies the appropriate AI agent.
2. The selected agent searches its corresponding CSV knowledge base.
3. If a matching answer is found, the response is returned directly from the CSV.
4. If no matching information is available, the query is forwarded to the Groq LLM.
5. The Groq LLM generates a context-aware response.

---

# 🧠 AI Workflow

```
                 User Query
                      │
                      ▼
               Triaging Agent
                      │
                      ▼
     Billing / Technical / Account /
      General / Escalation Agent
                      │
                      ▼
       Search CSV Knowledge Base
                      │
          ┌───────────┴───────────┐
          │                       │
     Match Found             No Match
          │                       │
          ▼                       ▼
  Return CSV Answer        Groq LLM Generates
                               AI Response
          └───────────┬───────────┘
                      ▼
             AI Response to User
                      │
                      ▼
      Store Conversation in SQLite
                      │
                      ▼
      Create Support Ticket (Optional)
```

---

# 💻 Technologies Used

## Frontend

- HTML5
- CSS3
- Bootstrap
- JavaScript

## Backend

- Python
- Flask

## AI Framework

- LangChain
- LangGraph

## LLM

- Groq API (Llama Model)

## Knowledge Base

- CSV Files (Domain-specific Knowledge Base)

## Database

- SQLite

## Other Libraries

- Python Dotenv
- UUID
- Jinja2

---

# 📂 Project Structure

```
Multi-Agent-Customer-Support/
│
├── agents/
│   ├── account.py
│   ├── billing.py
│   ├── escalation.py
│   ├── general.py
│   ├── technical.py
│   ├── triage.py
│
├── database/
│   └── support.db
│
├── db/
│   └── chroma.sqlite3
│
├── knowledge/
│   ├── account.csv
│   ├── billing.csv
│   ├── general.csv
│   └── technical.csv
│
├── logs/
│
├── services/
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── about.html
│   ├── base.html
│   ├── chat.html
│   ├── contact.html
│   ├── dashboard.html
│   ├── error.html
│   ├── history.html
│   ├── index.html
│   ├── login.html
│   ├── my_tickets.html
│   ├── register.html
│   ├── ticket_success.html
│   └── tickets.html
│
├── tests/
├── utils/
│
├── app.py
├── config.py
├── database.py
├── graph.py
├── memory.py
├── prompts.py
├── router.py
├── session_memory.py
├── state.py
├── requirements.txt
└── README.md
```

---

# ⚙️ How the System Works

1. User registers and logs into the application.
2. The user submits a support query.
3. The Triaging Agent classifies the query.
4. LangGraph routes the request to the appropriate specialized AI agent.
5. The selected agent searches its CSV knowledge base.
6. If a matching answer is found, it is returned directly to the user.
7. If no relevant answer is found, the Groq LLM generates a context-aware response.
8. The conversation is stored in the SQLite database.
9. If the issue remains unresolved, the user can create a support ticket.
10. The admin reviews the ticket and updates its status.
11. Users can monitor ticket progress through the **My Tickets** page.

---

# 📊 Dashboard

The Admin Dashboard provides:

- Total Conversations
- Billing Queries
- Technical Queries
- Account Queries
- General Queries
- Escalated Queries
- Open Tickets
- In Progress Tickets
- Resolved Tickets
- Recent Conversations

---

# 🎫 Ticket Management

## User

- Create Support Ticket
- View Personal Tickets
- Search Ticket by Ticket ID
- Track Ticket Status

## Admin

- View All Support Tickets
- Update Ticket Status
- Manage Customer Requests

---

# 🔐 Authentication

## User

- Register
- Login
- Logout

## Admin

Default Credentials

**Username**

```
admin
```

**Password**

```
admin123
```

---

# ▶️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/MultiAgent-AI-Customer-Support.git
```

Navigate to the project

```bash
cd MultiAgent-AI-Customer-Support
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
```

### Run the Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

# 📈 Future Enhancements

- Password Hashing using bcrypt
- Email Notifications for Ticket Updates
- File Attachments in Support Tickets
- Upgrade CSV Knowledge Base to ChromaDB
- Retrieval-Augmented Generation (RAG)
- Live Chat Support
- Docker Deployment
- Cloud Deployment

---

# 👩‍💻 Author

**Varsha Chavan**



Python | Flask | Machine Learning | Generative AI | LangChain | LangGraph

---

# 📄 License

This project is developed for educational and learning purposes.
