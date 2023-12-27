# 💉 Vaccination Scheduling System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![CLI](https://img.shields.io/badge/Interface-CLI-2D3748?style=for-the-badge\&logo=gnu-bash\&logoColor=white)
![Storage](https://img.shields.io/badge/Storage-JSON-FF9900?style=for-the-badge\&logo=json\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-4E9A06?style=for-the-badge)

*A secure Python-based vaccination management system featuring user authentication, appointment reservations, vaccination center management, and JSON-based persistent storage.*

</div>

---

## 📖 Overview

The Vaccination Scheduling System is a console-based application developed in Python to streamline the management of vaccination centers and appointment reservations. The system supports secure user registration, authentication, reservation handling, and administrative operations through a simple command-line interface.

This application represents my first university project, designed to establish a solid foundation in Python development and software engineering principles.

The project demonstrates practical software engineering concepts including authentication, data validation, file persistence, CRUD operations, and secure password management.

---

## 🎯 Project Highlights

* Implemented secure password storage using SHA-256 hashing
* Designed separate workflows for administrators and users
* Built a complete vaccination reservation lifecycle
* Applied regular-expression-based input validation
* Developed persistent file-based storage using JSON
* Implemented reservation approval and automated vaccination date assignment
* Utilized only Python standard libraries with no external dependencies
* Authentication & Authorization
* CRUD Operations
* Data Persistence
* Secure Password Hashing
* Input Validation
* Reservation Management

---

## ✨ Features

### 👤 User Features

* Secure account registration
* User authentication and login
* View available vaccination centers
* Browse available vaccine types
* Reserve a vaccination appointment
* View assigned vaccination date
* One active reservation per user

### 🔐 Administrator Features

* Administrator authentication
* Add new vaccination centers
* Remove existing vaccination centers
* Search centers by name
* View registered users
* Monitor reservation status
* Approve reservations
* Automatically assign vaccination dates

### 🛡️ Security & Validation

* SHA-256 password hashing
* Maximum login-attempt limitation
* Email validation using Regular Expressions
* Phone number validation
* National ID validation
* Duplicate account prevention
* Reservation integrity validation

---

## 🛠️ Technology Stack

| Component            | Technology                   |
| -------------------- | ---------------------------- |
| Programming Language | Python 3.8+                  |
| User Interface       | Command Line Interface (CLI) |
| Data Storage         | JSON Files                   |
| Security             | SHA-256 Hashing              |
| Validation           | Regular Expressions (Regex)  |
| Dependencies         | Python Standard Library      |

---

## 📁 Project Structure

```text
Vaccination-Scheduling-System/
│
├── Project.py
├── users.json
├── vaccination_centers.json
├── reservations.json
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🏗️ Architecture

The application follows a menu-driven architecture and is organized into four core components:

* Authentication & User Management
* Vaccination Center Management
* Reservation Management
* Data Persistence Layer (JSON Storage)

All data is stored locally using JSON files and loaded dynamically during runtime.

---

## ⚙️ System Workflow

1. User creates an account.
2. User logs into the system.
3. User browses vaccination centers.
4. User reserves a vaccination appointment.
5. Reservation is stored and awaits approval.
6. Administrator reviews reservations.
7. Administrator assigns a vaccination date.
8. User views the scheduled appointment.

---

## 🚀 Installation & Usage

### Prerequisites

* Python 3.8 or higher

### Clone the Repository

```bash
git clone https://github.com/yousefnathan/Vaccination-Scheduling-System.git
cd Vaccination-Scheduling-System
```

### Run the Application

```bash
python Project.py
```

### Initial Setup

On the first execution, the application automatically generates:

* `users.json`
* `vaccination_centers.json`
* `reservations.json`

with default values if they do not already exist.

---
## 📚 Learning Outcomes

This project demonstrates practical experience with:

* Authentication and Authorization
* Secure Password Management
* Input Validation Techniques
* CRUD Operations
* JSON-Based Data Persistence
* Command-Line Application Development
* Healthcare Reservation Workflows
* Software Engineering Best Practices

---

## 🔮 Future Enhancements

* [ ] Refactor the project using Object-Oriented Programming (OOP)
* [ ] Migrate JSON storage to SQLite or PostgreSQL
* [ ] Add email notifications for appointment updates
* [ ] Generate PDF vaccination certificates
* [ ] Develop a graphical user interface using Tkinter
* [ ] Build a web application version using Flask or Django
* [ ] Implement audit logging and advanced user roles

---

## 👨‍💻 Author

### Yousef Tarek

**AI & Data Science Student | Python Developer**

#### Areas of Interest

* Python Development
* Software Engineering
* Data Analysis
* Machine Learning

**GitHub:** https://github.com/yousefnathan

---

## 📄 License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute this project for educational or professional purposes.

---

<div align="center">

⭐ If you found this project useful, consider giving it a star.

Built with Python and designed to demonstrate secure reservation management, authentication, and software engineering fundamentals.

</div>
 