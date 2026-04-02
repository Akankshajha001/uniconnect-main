# Uni-Connect

## Campus Lost & Found + Notes Exchange Platform

A Streamlit-based campus utility platform with SQLite persistent storage, bcrypt password hashing, and a direct-contact claim system for lost & found items.

---

## Features

### Lost & Found System
- **Report Lost Items** with category, location, description, ID card number, and optional photo upload
- **Report Found Items** with phone number for direct contact by owner
- **Category-based security gate** — owner must first file a lost report in the same category before they can see the finder's contact details. Prevents misuse by random users.
- **Direct Contact flow** — owner contacts finder directly via phone/email, verifies ownership through real conversation
- **Manual Claim by Finder** — after verifying the owner (in person/call), the finder marks the item as claimed on the app
- **Big success popup** on claim with owner details
- **Separate tabs**: Report Lost, Report Found, Lost Items, Found Items, Claimed
- **Category filter** on Lost and Found item lists
- **Optional image upload** for both lost and found items

### Notes Exchange System
- **Upload notes** (PDF, DOC, DOCX, TXT) with subject, semester, and description
- **Browse all notes** with subject filter and sorting (recent, most downloaded, subject name)
- **Popular notes** tab showing most downloaded
- **Search** by subject, topic, description, or uploader name
- **Download tracking** with actual file download from server
- **Top Contributors leaderboard** with podium for top 3
- **File size validation** (max 10MB)
- **Description validation** (min 10 characters)

### User Management
- **Signup** with name, roll number (7 digits), email, and password
- **Login** via email or roll number
- **Password security**: bcrypt hashing (industry standard), SHA256 fallback
- **Password rules**: min 8 chars, uppercase, lowercase, digit, special character
- **Email validation**: checks domain against known providers (Gmail, Yahoo, Outlook, educational domains)
- **Session management** via Streamlit session state

### Dashboard
- Animated hero section with gradient background
- Feature cards for Lost & Found and Notes Exchange
- Quick action buttons when logged in (Report Lost, Report Found, Upload Notes, Browse Notes)

---

## Project Structure

```
uni-connect/
├── app.py                      # Main Streamlit entry point
├── requirements.txt            # Python dependencies
├── test_codes.py               # Database connectivity test script
│
├── database/                   # SQLite persistent storage
│   ├── __init__.py
│   ├── lost_found_db.py        # Lost & Found CRUD operations
│   ├── notes_db.py             # Notes CRUD operations
│   ├── users_db.py             # User auth & activity tracking
│   ├── lost_found.db           # SQLite database (auto-created)
│   ├── notes.db                # SQLite database (auto-created)
│   └── users.db                # SQLite database (auto-created)
│
├── services/                   # Business logic layer
│   ├── __init__.py
│   ├── lost_found_service.py   # Lost & Found operations
│   └── notes_service.py        # Notes exchange operations
│
├── ui/                         # Streamlit user interface
│   ├── __init__.py
│   ├── dashboard_ui.py         # Welcome page
│   ├── lost_found_ui.py        # Lost & Found interface
│   └── notes_ui.py             # Notes exchange interface
│
├── utils/                      # Helper utilities
│   ├── __init__.py
│   ├── validators.py           # Email, password, name, description validation
│   └── helpers.py              # Date formatting, text truncation, number formatting
│
├── uploaded_notes/             # Stored note files
└── uploaded_images/            # Stored item photos (auto-created)
```

---

## Architecture

```
User Action
    │
    ▼
Streamlit UI (ui/*.py)          ← Presentation layer
    │
    ▼
Service Layer (services/*.py)   ← Business logic
    │
    ▼
Database Layer (database/*.py)  ← SQLite CRUD operations
    │
    ▼
SQLite Files (.db)              ← Persistent storage
```

**Separation of concerns**: UI files never touch the database directly. Services handle all business logic. Database files handle only SQL operations.

---

## Lost & Found Claim Flow

```
Owner reports lost item (Report Lost tab)
    │
    ▼
Finder reports found item (Report Found tab, includes phone number)
    │
    ▼
Owner browses Found Items tab
    │
    ▼
System checks: does owner have a lost report in same category?
    │
    ├── NO  → Shows lock message: "Report your lost [Category] first"
    │
    └── YES → Shows "Contact Finder" button
                │
                ▼
            Owner clicks → Sees finder's name, email, phone
                │
                ▼
            Owner contacts finder directly (call/WhatsApp/email)
                │
                ▼
            Finder verifies ownership through conversation
                │
                ▼
            Finder clicks "Mark as Claimed" on the app
                │
                ▼
            Success popup → Item moves to Claimed tab
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Clone or navigate to the project
cd uni-connect

# Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# or: venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app opens at `http://localhost:8501` (or next available port).

### Dependencies

| Package | Purpose |
|---------|---------|
| streamlit | Web framework |
| bcrypt | Password hashing |
| pillow | Image handling |

SQLite is built into Python — no database server needed.

---

## How to Use

### 1. Sign Up & Login
- Open sidebar → Sign Up tab
- Enter name, 7-digit roll number, email, password
- Login with email and password

### 2. Report a Lost Item
- Go to Lost & Found → Report Lost tab
- Fill category, location, description
- Optionally upload a photo
- Submit

### 3. Report a Found Item
- Go to Lost & Found → Report Found tab
- Fill category, location, description, **phone number**
- Optionally upload a photo
- Submit

### 4. Claim Process
- Owner goes to Found Items tab
- If they have a matching lost report → "Contact Finder" button appears
- Click to see finder's contact details
- Contact finder directly to verify
- Finder marks as claimed from their view

### 5. Upload Notes
- Go to Notes Exchange → Upload Notes tab
- Fill subject, semester, name, description
- Upload file (PDF/DOC/TXT, max 10MB)
- Submit

### 6. Download Notes
- Browse All, Popular, or Search tabs
- Click Download button on any note card

---

## Key Functions

### Lost & Found Service
| Function | Purpose |
|----------|---------|
| `add_lost_item()` | Report a lost item |
| `add_found_item()` | Report a found item with verification data |
| `get_lost_items()` | Get all lost items |
| `get_found_items()` | Get all found items |
| `claim_item()` | Mark item as claimed, auto-claims matching lost reports |

### Notes Service
| Function | Purpose |
|----------|---------|
| `upload_note()` | Upload a new note |
| `get_notes_by_subject()` | Filter notes by subject |
| `get_all_notes_list()` | Get all notes |
| `get_popular_notes()` | Get most downloaded notes |
| `search_notes()` | Search by subject/topic/description/uploader |
| `get_top_contributors()` | Leaderboard by upload count |
| `increment_download_count()` | Track downloads |

### Validators
| Function | Rules |
|----------|-------|
| `validate_email()` | Real domain check (Gmail, Yahoo, Outlook, .edu, .ac.in) |
| `validate_roll_no()` | Exactly 7 digits |
| `validate_password()` | 8+ chars, uppercase, lowercase, digit, special char |
| `validate_name()` | 2-100 chars, letters/spaces/dots/hyphens only |
| `validate_description()` | 10-500 characters |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend & Backend | Streamlit (Python) |
| Database | SQLite3 (built-in) |
| Password Security | bcrypt / SHA256 fallback |
| File Storage | Local filesystem |
| Language | Python 3 |

---

## Author

- **Developer**: group 11-akanksha,kamya,rashi,yashita
- **Project**: Uni-Connect v2.0
- **Date**: March 2026
