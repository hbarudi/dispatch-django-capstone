# Dispatch Django – Capstone News Application

## Project Overview
Dispatch Django is a robust, enterprise-level news platform built with
Django and MariaDB. It empowers independent journalists to reach
audiences directly while maintaining journalistic standards through a
curated editor approval workflow.

This project was developed as a Capstone Project for HyperionDev,
demonstrating competencies in custom user authentication, granular
permission management, third-party API integration, and RESTful
service design.

## Test Accounts (Dummy Users)
For testing purposes, the following accounts have been pre-configured in the provided `db_backup.json`:

| Username          | Role       | Password                | Purpose                         |
|:------------------|:-----------|:------------------------|:--------------------------------|
| **admin**         | Superuser  | DispatchAdminSecure789! | Full site management.           |
| **EdithEditor**   | EDITOR     | EdithPass2025!          | Review Queue & Approval.        |
| **JoeJournalist** | JOURNALIST | JoePass2025!            | Authoring Articles/Newsletters. |
| **RitaReader**    | READER     | RitaPass2025!           | Subscriptions & Feed viewing.   |

## Core Features

### 1. Role-Based Access Control (RBAC)
The system uses a Custom User Model with four distinct roles:
*   **Administrator**: Full system control via the Django Admin.
*   **Editor**: Creates publishers and approves/unpublishes articles.
*   **Journalist**: Authors, edits, and deletes articles/newsletters.
*   **Reader**: Follows sources and consumes curated content.

### 2. Publisher Management
Editors can create publishers, and editors/journalists can join publishers.
Readers can subscribe to publishers to curate their feeds.

### 3. Automated Dissemination
Upon article approval by an Editor, the system will automatically:
*   Sends email notifications to all journalists and publisher
    subscribers.
*   Posts a "Breaking News" update to a linked X (formerly Twitter)
    account via the X HTTP API.

### 4. Subscriber-Exclusive Content
While Articles are public, **Newsletters** are exclusive to
subscribers. Readers can follow specific Journalists or Publishers
to unlock their personal newsletter feeds.
Journalists can create, edit, and delete their newsletters.

### 5. RESTful API
A secure API endpoint (`/api/articles/`) provides:
*   Subscription-aware content delivery (clients only see what they
    follow).
*   Keyword search functionality.
*   Nested serialization of authors and publishers.

## Technical Stack
*   **Backend**: Python 3.13 / Django 6.0
*   **API**: Django REST Framework (DRF)
*   **Database**: MariaDB (Production-ready)
*   **Integration**: requests-oauthlib (X API v2)
*   **Styling**: Custom CSS (Dark Brown & Vivid Orange Theme)

## Installation & Setup

1.  **Clone the repository and enter the directory.**
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure MariaDB:**
    Create a database named `dispatch_db` and update the `DATABASES`
    credentials in `dispatch_core/settings.py`.
5.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```
6.  **Create Superuser:**
    ```bash
    python manage.py createsuperuser
    ```
7.  **Launch Server:**
    ```bash
    python manage.py runserver 8001
    ```

## Testing
To run the automated test suite for the API and subscription logic:
```bash
python manage.py test dispatch_app.unit_tests
```

---

## Project Updated:
* CRUD support for articles and newsletters for journalists.
* Publisher flow: editors create publishers, and editors/journalists can join.

**Built by Hashem Barudi as part of the HyperionDev Django News Application Capstone Project.**

## Documentation (Sphinx)
This project includes developer documentation generated with Sphinx.

### Build the docs locally (HTML)
From the project root:
```bash
cd docs
.\make.bat html
``` 

Then open:

- `docs/build/html/index.html`

