import database
import student


def main():
    connected, message = database.test_connection()
    if not connected:
        print(f"deli makakonekta sa XAMPP MySQL: {message}")
        print("make sure ba naka-start ang MySQL at na-import ang schema.sql.")
        return
    print(message)

    print("\n=== STUDENT ADDING SYSTEM ===")
    while True:
        print("\n[1] Add a Student po")
        print("[2] Viaw all tha student nga na add")
        print("[3] Search a student")
        print("[4] edit the student info boss")
        print("[5] delete student")
        print("[6] delete all students")
        print("[0] Exit ka boss?")
        choice = input("Piliin: ").strip()

        if choice == "1":
            student.add_student()
        elif choice == "2":
            student.show_students()
        elif choice == "3":
            student.search_student()
        elif choice == "4":
            student.edit_student()
        elif choice == "5":
            student.remove_student()
        elif choice == "6":
            student.remove_all_students()
        elif choice == "0":
            print("Salamat! Paalam.")
            break
        else:
            print("Hindi wastong pagpili or mali ka. Pumili ng 1, 2, 3, 4, 5, 6, o 0.")


if __name__ == "__main__":
    main()
