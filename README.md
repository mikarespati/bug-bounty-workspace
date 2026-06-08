# 🐞 Bug Bounty Workspace Assistant

A personal vulnerability management platform built with Flask for bug bounty hunters, penetration testers, and cybersecurity learners.

## 🚀 Features

### 🎯 Target Management

* Create, edit, and delete bug bounty targets
* Define in-scope and out-of-scope assets
* Track target status (Active, Paused, Completed)
* Set priority levels

### 📝 Notes Management

* Create and organize notes per target
* Pin important notes
* Categorize notes:

  * General
  * Scope Info
  * API Pattern
  * Testing Notes
  * Warning

### 🔌 Endpoint Management

* Store discovered endpoints
* Track HTTP methods
* Record status codes
* Mark authentication requirements
* Add technology stack information
* Attach endpoint-specific notes

### 🐞 Findings Management

* Record discovered vulnerabilities
* Track severity levels
* Associate findings with endpoints
* Maintain vulnerability details
* Track finding status

## 🏗️ Tech Stack

* Python 3
* Flask
* SQLAlchemy
* SQLite
* Bootstrap 5
* Jinja2

## 📂 Project Structure

```text
bug-bounty-workspace/
│
├── app/
│   ├── routes/
│   ├── templates/
│   ├── models.py
│   ├── config.py
│   └── __init__.py
│
├── instance/
│   └── database.db
│
├── run.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

Clone repository:

```bash
git clone https://github.com/mikarespati/bug-bounty-workspace.git
cd bug-bounty-workspace
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

Linux / WSL:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

## 🗺️ Development Roadmap

### Completed

* [x] Sprint 1 - Foundation
* [x] Sprint 2 - Target Management
* [x] Sprint 3 - Notes Management
* [x] Sprint 4 - Endpoint Management
* [x] Sprint 5 - Findings Management

### Upcoming

* [ ] Sprint 6 - Finding Detail Management
* [ ] Sprint 7 - Reporting System
* [ ] Sprint 8 - Dashboard Analytics
* [ ] Sprint 9 - Search & Filters
* [ ] Sprint 10 - AI Workspace Assistant

## 🎯 Purpose

This project is being developed as a portfolio project and learning platform for bug bounty workflows, vulnerability management, and secure software development.

## 📜 License

MIT License

---

Built with ❤️ by Mika Respati
