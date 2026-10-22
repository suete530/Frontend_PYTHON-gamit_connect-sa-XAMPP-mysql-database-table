import mysql.connector

import database


def ask_required(prompt, max_length):
    while True:
        value = input(prompt).strip()
        if not value:
            print("Kailangan itong punan.")
        elif len(value) > max_length:
            print(f"Hindi dapat lumampas sa {max_length} characters.")
        else:
            return value


def is_valid_email(email):
    email_name, separator, email_domain = email.partition("@")
    return bool(separator and email_name and "." in email_domain)


def ask_year_level(prompt="Year level (1-4): "):
    while True:
        year_level = input(prompt).strip()
        if year_level in {"1", "2", "3", "4"}:
            return int(year_level)
        print("Pumili ng year level mula 1 hanggang 4.")


def ask_age(prompt="Edad: "):
    while True:
        age = input(prompt).strip()
        if age.isdigit() and 1 <= int(age) <= 120:
            return int(age)
        print("Ilagay ang tamang edad (1-120).")


def ask_civil_status(prompt="Single ka ba? (o/h): "):
    while True:
        answer = input(prompt).strip().lower()
        if answer in {"o", "oo", "y", "yes"}:
            return "Single"
        if answer in {"h", "hindi", "n", "no"}:
            return "Hindi Single"
        print("Sagutin ng o (oo) o h (hindi).")


def get_student_details():
    student = {
        "student_number": ask_required("Student number: ", 30),
        "full_name": ask_required("Buong pangalan: ", 150),
        "email": ask_required("Email: ", 120),
        "course": ask_required("Course/program: ", 120),
    }

    if not is_valid_email(student["email"]):
        print("Hindi wastong email address.")
        return None

    student["year_level"] = ask_year_level()
    student["section"] = ask_required("Section: ", 30)
    student["age"] = ask_age()
    student["civil_status"] = ask_civil_status()
    student["address"] = ask_required("Taga saan ka: ", 255)
    return student


def display_student(student):
    print(
        f"\nStudent number: {student['student_number']}\n"
        f"Pangalan:       {student['full_name']}\n"
        f"Email:          {student['email']}\n"
        f"Course:         {student['course']}\n"
        f"Year level:     {student['year_level']}\n"
        f"Section:        {student['section']}\n"
        f"Edad:           {student['age']}\n"
        f"Civil status:   {student['civil_status']}\n"
        f"Taga saan:      {student['address']}"
    )


def add_student():
    print("\n--- Magdagdag ng estudyante ---")
    details = get_student_details()
    if details is None:
        return

    try:
        student_id = database.insert_student(details)
        print(f"Matagumpay na nai-save ang student record. ID: {student_id}")
    except mysql.connector.IntegrityError:
        print("May record na gamit ang student number na iyan.")
    except mysql.connector.Error as error:
        print(f"Hindi nai-save ang record: {error}")


def show_students():
    try:
        students = database.get_all_students()
    except mysql.connector.Error as error:
        print(f"Hindi makuha ang student records: {error}")
        return

    print("\n--- Mga naka-enroll na estudyante ---")
    if not students:
        print("Wala pang student records.")
        return

    for student in students:
        display_student(student)


def search_student():
    student_number = ask_required("Student number na hahanapin: ", 30)
    try:
        student = database.get_student_by_number(student_number)
    except mysql.connector.Error as error:
        print(f"Hindi mahanap ang record: {error}")
        return

    if student is None:
        print("Walang estudyanteng may student number na iyan.")
        return

    display_student(student)


def edit_student():
    student_number = ask_required("Student number na ie-edit: ", 30)
    try:
        current = database.get_student_by_number(student_number)
    except mysql.connector.Error as error:
        print(f"Hindi makuha ang record: {error}")
        return

    if current is None:
        print("Walang estudyanteng may student number na iyan.")
        return

    print("\nIwanang blangko ang field kung hindi ito babaguhin.")
    updated = {}
    for field, label, limit in (
        ("full_name", "Buong pangalan", 150),
        ("email", "Email", 120),
        ("course", "Course/program", 120),
        ("section", "Section", 30),
        ("address", "Taga saan", 255),
    ):
        value = input(f"{label} [{current[field]}]: ").strip()
        if len(value) > limit:
            print(f"Hindi dapat lumampas sa {limit} characters. Walang binago.")
            return
        updated[field] = value or current[field]

    if not is_valid_email(updated["email"]):
        print("Hindi wastong email address. Walang binago.")
        return

    year_level = input(f"Year level (1-4) [{current['year_level']}]: ").strip()
    if year_level:
        if year_level not in {"1", "2", "3", "4"}:
            print("Pumili ng year level mula 1 hanggang 4. Walang binago.")
            return
        updated["year_level"] = int(year_level)
    else:
        updated["year_level"] = current["year_level"]

    age = input(f"Edad [{current['age']}]: ").strip()
    if age:
        if not age.isdigit() or not 1 <= int(age) <= 120:
            print("Ilagay ang tamang edad (1-120). Walang binago.")
            return
        updated["age"] = int(age)
    else:
        updated["age"] = current["age"]

    civil_status = input(
        f"Single ka ba? (o/h) [{current['civil_status']}]: "
    ).strip().lower()
    if civil_status:
        if civil_status in {"o", "oo", "y", "yes"}:
            updated["civil_status"] = "Single"
        elif civil_status in {"h", "hindi", "n", "no"}:
            updated["civil_status"] = "Hindi Single"
        else:
            print("Sagutin ng o (oo) o h (hindi). Walang binago.")
            return
    else:
        updated["civil_status"] = current["civil_status"]

    try:
        updated_record = database.update_student(student_number, updated)
    except mysql.connector.Error as error:
        print(f"Hindi na-update ang record: {error}")
        return

    if updated_record:
        print("Matagumpay na na-update ang student record.")
    else:
        print("Walang nabagong student record.")


def remove_student():
    student_number = ask_required("Student number na buburahin: ", 30)
    try:
        current = database.get_student_by_number(student_number)
    except mysql.connector.Error as error:
        print(f"Hindi makuha ang record: {error}")
        return

    if current is None:
        print("Walang estudyanteng may student number na iyan.")
        return

    display_student(current)
    confirmation = input("Sigurado ka bang buburahin ito? (o/h): ").strip().lower()
    if confirmation not in {"o", "oo", "y", "yes"}:
        print("Kinansela ang pagbura.")
        return

    try:
        deleted = database.delete_student(student_number)
    except mysql.connector.Error as error:
        print(f"Hindi nabura ang record: {error}")
        return

    if deleted:
        print("Matagumpay na nabura ang student record.")
    else:
        print("Wala nang student record na buburahin.")


def remove_all_students():
    confirmation = input(
        "Sigurado ka bang buburahin ang LAHAT ng student records? (o/h): "
    ).strip().lower()
    if confirmation not in {"o", "oo", "y", "yes"}:
        print("Kinansela ang pagbura ng lahat ng records.")
        return

    try:
        deleted_count = database.delete_all_students()
    except mysql.connector.Error as error:
        print(f"Hindi nabura ang student records: {error}")
        return

    if deleted_count:
        print(f"Matagumpay na nabura ang {deleted_count} student records.")
    else:
        print("Walang student records na buburahin.")
