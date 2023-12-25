import json
import os
import re
import random
import datetime
import hashlib

# ── Constants ────────────────────────────────────────────────────────────────
USERS_FILE             = "users.json"
CENTERS_FILE           = "vaccination_centers.json"
RESERVATIONS_FILE      = "reservations.json"
ADMIN_PASSWORD         = hashlib.sha256("admin123".encode()).hexdigest()
MAX_LOGIN_ATTEMPTS     = 3


# ── File helpers ──────────────────────────────────────────────────────────────
def _load(filepath):
    """Load a JSON file; return empty list if missing."""
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return []

def _save(filepath, data):
    """Save data to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def init_data():
    """Create default centers file if it doesn't exist yet."""
    if not os.path.exists(CENTERS_FILE):
        default_centers = [
            {"id": 1, "name": "Center A", "address": "123 Main Street, Cairo",      "vaccines": ["Pfizer", "Moderna"]},
            {"id": 2, "name": "Center B", "address": "456 Second Avenue, Alexandria","vaccines": ["AstraZeneca", "Johnson & Johnson"]}
        ]
        _save(CENTERS_FILE, default_centers)
    if not os.path.exists(USERS_FILE):
        _save(USERS_FILE, [])
    if not os.path.exists(RESERVATIONS_FILE):
        _save(RESERVATIONS_FILE, [])


# ── Input helpers ─────────────────────────────────────────────────────────────
def _ask(prompt, validator=None, error_msg="Invalid input."):
    """Prompt until the user provides valid non-empty input."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("This field cannot be empty.")
            continue
        if validator and not validator(value):
            print(error_msg)
            continue
        return value

def _ask_int(prompt):
    """Prompt until the user enters a valid integer."""
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            return int(raw)
        print("Please enter a valid number.")

def _ask_date(prompt):
    """Prompt until the user enters a valid YYYY-MM-DD date."""
    while True:
        raw = input(prompt).strip()
        try:
            datetime.date.fromisoformat(raw)
            return raw
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD format.")

def _confirm(prompt):
    """Ask a yes/no question; return True for 'y'."""
    return input(f"{prompt} (y/n): ").strip().lower() == "y"

def _hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ── Validators ────────────────────────────────────────────────────────────────
def _valid_email(email):
    return bool(re.match(r"^[\w.\-+]+@[\w\-]+\.[a-zA-Z]{2,}$", email))

def _valid_phone(phone):
    return bool(re.match(r"^\+?[\d\s\-]{7,15}$", phone))

def _valid_national_id(nid):
    return bool(re.match(r"^\d{10,20}$", nid))


# ── Auth ──────────────────────────────────────────────────────────────────────
def register_user():
    """Register a new user and save to file."""
    print("\n── Register ──────────────────────────────────")
    name        = _ask("Full name: ")
    email       = _ask("Email: ",       _valid_email,       "Enter a valid email address.")
    phone       = _ask("Phone: ",       _valid_phone,       "Enter a valid phone number (7-15 digits).")
    national_id = _ask("National ID: ", _valid_national_id, "National ID must be 10-20 digits.")
    password    = _ask("Password (min 6 chars): ",
                       lambda p: len(p) >= 6, "Password must be at least 6 characters.")

    users = _load(USERS_FILE)

    # Check for duplicate email
    if any(u["email"] == email for u in users):
        print("An account with that email already exists.")
        return

    user_id = max((u["id"] for u in users), default=0) + 1
    users.append({
        "id":          user_id,
        "name":        name,
        "email":       email,
        "password":    _hash(password),
        "phone":       phone,
        "national_id": national_id,
    })
    _save(USERS_FILE, users)
    print(f"Registered successfully! Your user ID is {user_id}.")


def login_admin():
    """Authenticate the admin; allow up to MAX_LOGIN_ATTEMPTS tries."""
    print("\n── Admin Login ───────────────────────────────")
    for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
        password = input("Admin password: ")
        if _hash(password) == ADMIN_PASSWORD:
            print("Login successful.")
            return True
        print(f"Wrong password. ({attempt}/{MAX_LOGIN_ATTEMPTS})")
    print("Too many failed attempts.")
    return False


def login_user():
    """Authenticate a regular user. Returns user dict on success, None on failure."""
    print("\n── User Login ────────────────────────────────")
    for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
        email    = input("Email: ").strip()
        password = input("Password: ")
        users    = _load(USERS_FILE)
        for user in users:
            if user["email"] == email and user["password"] == _hash(password):
                print(f"Welcome, {user['name']}!")
                return user
        print(f"Wrong email or password. ({attempt}/{MAX_LOGIN_ATTEMPTS})")
    print("Too many failed attempts.")
    return None


# ── Admin features ────────────────────────────────────────────────────────────
def add_or_remove_center():
    """Sub-menu: add or remove a vaccination center."""
    print("\n1. Add a new center")
    print("2. Remove an existing center")
    print("3. Back")
    choice = input("Choice (1-3): ")

    if choice == "1":
        name     = _ask("Center name: ")
        address  = _ask("Address: ")
        vaccines = [v.strip()
                    for v in _ask("Vaccines (comma-separated): ").split(",")
                    if v.strip()]
        if not vaccines:
            print("You must enter at least one vaccine.")
            return
        centers = _load(CENTERS_FILE)
        new_id  = max((c["id"] for c in centers), default=0) + 1
        centers.append({"id": new_id, "name": name,
                         "address": address, "vaccines": vaccines})
        _save(CENTERS_FILE, centers)
        print(f"Center '{name}' added with ID {new_id}.")

    elif choice == "2":
        centers = _load(CENTERS_FILE)
        if not centers:
            print("No centers on file.")
            return
        center_id = _ask_int("Enter center ID to remove: ")
        target    = next((c for c in centers if c["id"] == center_id), None)
        if not target:
            print("Center not found.")
            return
        if not _confirm(f"Remove '{target['name']}'?"):
            print("Cancelled.")
            return
        _save(CENTERS_FILE, [c for c in centers if c["id"] != center_id])
        print("Center removed.")

    elif choice == "3":
        return
    else:
        print("Invalid choice.")


def search_center_by_name():
    """Search for a vaccination center by name (case-insensitive)."""
    name    = input("Enter center name to search: ").strip().lower()
    centers = _load(CENTERS_FILE)
    found   = [c for c in centers if c["name"].lower() == name]

    if found:
        c = found[0]
        print(f"\nID:       {c['id']}")
        print(f"Name:     {c['name']}")
        print(f"Address:  {c['address']}")
        print(f"Vaccines: {', '.join(c['vaccines'])}")
    else:
        print("No center found with that name.")


def list_users_and_reservations():
    """Print every registered user and their reservation status."""
    users        = _load(USERS_FILE)
    reservations = _load(RESERVATIONS_FILE)
    centers      = _load(CENTERS_FILE)

    if not users:
        print("No users registered yet.")
        return

    center_map = {c["id"]: c["name"] for c in centers}

    print("\n── Registered Users ──────────────────────────")
    for u in users:
        print(f"ID: {u['id']}  |  Name: {u['name']}  |  "
              f"Email: {u['email']}  |  Phone: {u['phone']}")

        res = next((r for r in reservations if r["user_id"] == u["id"]), None)
        if res:
            center_name = center_map.get(res["center_id"], "Unknown")
            date_str    = res.get("date") or "pending"
            print(f"   ↳ Reservation: {res['vaccine']} at "
                  f"{center_name} | Date: {date_str}")
        else:
            print("   ↳ No reservation")
        print("-" * 46)


def accept_reservation():
    """Auto-generate a vaccination date (10–30 days from today) for a user's reservation."""
    reservations = _load(RESERVATIONS_FILE)
    user_id      = _ask_int("Enter user ID: ")

    res = next((r for r in reservations if r["user_id"] == user_id), None)
    if not res:
        print("No reservation found for that user.")
        return

    if res["date"]:
        print(f"This user already has an assigned date: {res['date']}")
        return

    delta          = random.randint(10, 30)
    assigned_date  = (datetime.date.today() + datetime.timedelta(days=delta)).strftime("%Y-%m-%d")
    res["date"]    = assigned_date
    _save(RESERVATIONS_FILE, reservations)
    print(f"Reservation accepted! Assigned date: {assigned_date}")


# ── User features ─────────────────────────────────────────────────────────────
def view_centers():
    """Display all vaccination centers."""
    centers = _load(CENTERS_FILE)
    if not centers:
        print("No vaccination centers available yet.")
        return
    print("\n── Vaccination Centers ───────────────────────")
    for c in centers:
        print(f"ID: {c['id']}  |  {c['name']}  |  {c['address']}")
        print(f"   Vaccines: {', '.join(c['vaccines'])}")
    print("-" * 46)


def reserve_vaccination(user):
    """Allow the user to reserve a vaccination slot."""
    reservations = _load(RESERVATIONS_FILE)

    # One reservation per user
    if any(r["user_id"] == user["id"] for r in reservations):
        print("You already have a reservation. View it with option 3.")
        return

    view_centers()
    centers = _load(CENTERS_FILE)
    if not centers:
        return

    center_id = _ask_int("Center ID: ")
    center    = next((c for c in centers if c["id"] == center_id), None)

    if not center:
        print("Center not found.")
        return

    print(f"Available vaccines: {', '.join(center['vaccines'])}")
    vaccine = _ask("Vaccine name: ")

    # Case-insensitive check
    matched = next((v for v in center["vaccines"] if v.lower() == vaccine.lower()), None)
    if not matched:
        print("That vaccine is not available at this center.")
        return

    reservations.append({
        "user_id":   user["id"],
        "center_id": center_id,
        "vaccine":   matched,   # store the correctly-cased name
        "date":      None,
    })
    _save(RESERVATIONS_FILE, reservations)
    print("Reservation made! The admin will assign your date.")


def view_vaccination_date(user):
    """Show the user their assigned vaccination date."""
    reservations = _load(RESERVATIONS_FILE)
    res = next((r for r in reservations if r["user_id"] == user["id"]), None)

    if not res:
        print("You have no reservation yet.")
    elif res["date"]:
        centers     = _load(CENTERS_FILE)
        center_name = next(
            (c["name"] for c in centers if c["id"] == res["center_id"]),
            "Unknown"
        )
        print(f"Your vaccination: {res['vaccine']} at {center_name} "
              f"on {res['date']}.")
    else:
        print("Your reservation is pending — the admin hasn't set a date yet.")


# ── Menus ─────────────────────────────────────────────────────────────────────
def admin_menu():
    while True:
        print("\n── Admin Menu ────────────────────────────────")
        print("1. Add / Remove a vaccination center")
        print("2. Search for a center by name")
        print("3. List all users and reservations")
        print("4. Accept a reservation and assign a date")
        print("5. Logout")
        choice = input("Choice (1-5): ")

        if   choice == "1": add_or_remove_center()
        elif choice == "2": search_center_by_name()
        elif choice == "3": list_users_and_reservations()
        elif choice == "4": accept_reservation()
        elif choice == "5":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")


def user_menu(user):
    while True:
        print(f"\n── User Menu ({user['name']}) ────────────────────")
        print("1. View vaccination centers")
        print("2. Reserve a vaccination")
        print("3. View my vaccination date")
        print("4. Logout")
        choice = input("Choice (1-4): ")

        if   choice == "1": view_centers()
        elif choice == "2": reserve_vaccination(user)
        elif choice == "3": view_vaccination_date(user)
        elif choice == "4":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")


# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    init_data()  # Create default files if they don't exist
    while True:
        print("\n══ Vaccination Scheduling System ══════════════")
        print("1. Register")
        print("2. Login as admin")
        print("3. Login as user")
        print("4. Exit")
        choice = input("Choice (1-4): ")

        if choice == "1":
            register_user()
        elif choice == "2":
            if login_admin():
                admin_menu()
        elif choice == "3":
            user = login_user()
            if user:
                user_menu(user)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()