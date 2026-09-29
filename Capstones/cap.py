from dataclasses import dataclass
from functools import wraps
import time

# --- Custom Exceptions ---
class StudentNotFoundError(Exception): pass
class InvalidInputError(Exception): pass
class InvalidChoiceError(Exception): pass

# --- Py1.4 Dataclass ---
@dataclass
class StudentInfo:
    college: str = "KMEC"
    course: str = "CSE"

# --- Py1.5 Decorator ---
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        # --- Py1.13 Profiling ---
        print(f"\nExecution Time: {time.time()-start:.6f} seconds")
        return result
    return wrapper

# --- Py1.6 Parameterized Decorator ---
def log(message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"\n[{message}] Started")
            result = func(*args, **kwargs)
            print(f"[{message}] Completed")
            return result
        return wrapper
    return decorator

class StudentOperations:
    def __init__(self):
        self.students = []
        self.info = StudentInfo()

    # --- Py1.2 **kwargs ---
    def create_student(self, **details):
        return {
            "id": details["id"],
            "name": details["name"],
            "marks": details["marks"]
        }

    # --- Py1.2 *args ---
    def add_students(self, *students):
        for student in students:
            self.students.append(student)

    def add_student(self):
        print("\nAdd Student\n" + "-"*30)
        try:
            id_input = input("Enter ID: ")
            if not id_input.isdigit():
                raise InvalidInputError("ID must be digits only.")
            name = input("Enter Name: ")
            marks_input = input("Enter Marks: ")
            try:
                marks = float(marks_input)
            except ValueError:
                raise InvalidInputError("Marks must be a valid number.")

            student = self.create_student(id=int(id_input), name=name, marks=marks)
            self.add_students(student)
            print("\nStudent Added Successfully.")
        except InvalidInputError as e:
            print(f"\nError: {e}")

    # --- Py1.7 Iterator ---
    def display_students(self):
        if not self.students:
            print("\nNo Students Available")
            return

        iterator = iter(self.students)
        print("\nStudent Records\n" + "-" * 30)
        try:
            while True:
                student = next(iterator)
                self._print_student(student)
        except StopIteration:
            pass

    # --- Py1.7 Generator ---
    def passing_students(self):
        for student in self.students:
            if student["marks"] >= 40:
                yield student

    def show_passing_students(self):
        print("\nPassing Students")
        found = False
        for student in self.passing_students():
            self._print_student(student)
            found = True
        if not found:
            print("No Passing Students")

    def search_student(self):
        try:
            sid = input("Enter Student ID: ")
            if not sid.isdigit():
                raise InvalidInputError("ID must be digits.")
            for student in self.students:
                if student["id"] == int(sid):
                    print("\nStudent Found")
                    self._print_student(student)
                    return
            raise StudentNotFoundError("Student Not Found")
        except (StudentNotFoundError, InvalidInputError) as e:
            print(f"\nError: {e}")

    # --- Py1.1 List Comprehension ---
    def student_names(self):
        names = [s["name"] for s in self.students]
        print("\nStudent Names:", names)

    def update_marks(self):
        try:
            sid = input("Enter Student ID: ")
            if not sid.isdigit():
                raise InvalidInputError("ID must be digits.")
            for student in self.students:
                if student["id"] == int(sid):
                    marks_input = input("Enter New Marks: ")
                    try:
                        student["marks"] = float(marks_input)
                    except ValueError:
                        raise InvalidInputError("Marks must be a valid number.")
                    print("\nMarks Updated Successfully.")
                    return
            raise StudentNotFoundError("Student Not Found")
        except (StudentNotFoundError, InvalidInputError) as e:
            print(f"\nError: {e}")

    def delete_student(self):
        try:
            sid = input("Enter Student ID: ")
            if not sid.isdigit():
                raise InvalidInputError("ID must be digits.")
            for student in self.students:
                if student["id"] == int(sid):
                    self.students.remove(student)
                    print("\nStudent Deleted Successfully.")
                    return
            raise StudentNotFoundError("Student Not Found")
        except (StudentNotFoundError, InvalidInputError) as e:
            print(f"\nError: {e}")

    # --- Py1.1 Lambda ---
    def show_topper(self):
        if not self.students:
            print("\nNo Students Available")
            return
        topper = max(self.students, key=lambda s: s["marks"])
        print("\nTopper")
        self._print_student(topper)

    def _print_student(self, student):
        print("-" * 30)
        print(f"ID    : {student['id']}")
        print(f"Name  : {student['name']}")
        print(f"Marks : {student['marks']}")
        print("-" * 30)

# --- Py1.3 Inheritance ---
class StudentMenu(StudentOperations):
    # --- Py1.8 Context Manager ---
    @timer
    @log("SAVE REPORT")
    def save_report(self):
        if not self.students:
            print("\nNo Students Available")
            return
        with open("students.txt", "w") as file:
            for s in self.students:
                file.write(f"{s['id']} {s['name']} {s['marks']}\n")
        print("\nReport Saved Successfully")

    def menu(self):
        while True:
            print("\n========== STUDENT RESULT MANAGEMENT ==========")
            options = ["Add Student", "Display Students", "Search Student", "Update Marks", "Delete Student", "Show Passing Students", "Show Topper", "Student Names", "Save Report", "Exit"]
            for i, opt in enumerate(options, 1): print(f"{i}. {opt}")

            try:
                choice_input = input("\nEnter Choice : ")
                if not choice_input.isdigit(): raise InvalidInputError("Enter Digits Only")
                choice = int(choice_input)
                if not (1 <= choice <= 10): raise InvalidChoiceError("Enter Any Given Choice Only (1-10)")
            except (InvalidInputError, InvalidChoiceError) as e:
                print(f"\nError: {e}")
                continue

            if choice == 10:
                print("\nThank You")
                break

            if choice == 1: self.add_student()
            elif choice == 2: self.display_students()
            elif choice == 3: self.search_student()
            elif choice == 4: self.update_marks()
            elif choice == 5: self.delete_student()
            elif choice == 6: self.show_passing_students()
            elif choice == 7: self.show_topper()
            elif choice == 8: self.student_names()
            elif choice == 9: self.save_report()

def main():
    system = StudentMenu()
    system.menu()

if __name__ == "__main__":
    main()
