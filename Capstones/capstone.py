from dataclasses import dataclass
from functools import wraps
import time


class StudentNotFoundError(Exception):
    pass


@dataclass
class Student:

    student_id: int
    name: str
    branch: str
    marks: float





class StudentManagement:

    def __init__(self):

        self.students: list[Student] = []

    def create_student(
        self,
        **details
    ) -> Student:

        return Student(

            details["student_id"],
            details["name"],
            details["branch"],
            details["marks"]

        )

    def add_students(
        self,
        *students: Student
    ) -> None:

        for student in students:

            self.students.append(student)

    def add_student(self):

        print("\nAdd Student")
        print("-" * 30)

        student_id = int(input("Enter ID : "))
        name = input("Enter Name : ")
        branch = input("Enter Branch : ")
        marks = float(input("Enter Marks : "))

        student = self.create_student(

            student_id=student_id,
            name=name,
            branch=branch,
            marks=marks

        )

        self.add_students(student)

        print("\nStudent Added Successfully.")
        
class StudentIterator:

    def __init__(self, students: list[Student]):

        self.students = students
        self.index = 0

    def __iter__(self):

        return self

    def __next__(self):

        if self.index >= len(self.students):

            raise StopIteration

        student = self.students[self.index]

        self.index += 1

        return student


class StudentManagement(StudentManagement):

    def find_student(self, student_id: int) -> Student:

        for student in self.students:

            if student.student_id == student_id:

                return student

        raise StudentNotFoundError("Student Not Found")

    def display_students(self):

        if len(self.students) == 0:

            print("\nNo Students Found.")
            return

        iterator = StudentIterator(self.students)

        print("\nStudent Records")
        print("-" * 40)

        for student in iterator:

            print(f"ID     : {student.student_id}")
            print(f"Name   : {student.name}")
            print(f"Branch : {student.branch}")
            print(f"Marks  : {student.marks}")
            print("-" * 40)

    def search_student(self):

        try:

            student_id = int(input("Enter Student ID : "))

            student = self.find_student(student_id)

            print("\nStudent Found")
            print(f"ID     : {student.student_id}")
            print(f"Name   : {student.name}")
            print(f"Branch : {student.branch}")
            print(f"Marks  : {student.marks}")

        except StudentNotFoundError as e:

            print(e)

    def update_marks(self):

        try:

            student_id = int(input("Enter Student ID : "))

            student = self.find_student(student_id)

            student.marks = float(input("Enter New Marks : "))

            print("\nMarks Updated Successfully.")

        except StudentNotFoundError as e:

            print(e)

    def delete_student(self):

        try:

            student_id = int(input("Enter Student ID : "))

            student = self.find_student(student_id)

            self.students.remove(student)

            print("\nStudent Deleted Successfully.")

        except StudentNotFoundError as e:

            print(e)

    def passing_students(self):

        for student in self.students:

            if student.marks >= 40:

                yield student

    def show_topper(self):

        if len(self.students) == 0:

            print("\nNo Students Found.")
            return

        topper = sorted(

            self.students,

            key=lambda student: student.marks,

            reverse=True

        )[0]

        print("\nTopper")
        print("-" * 30)
        print(f"Name  : {topper.name}")
        print(f"Marks : {topper.marks}")

    def student_names(self):

        names = [

            student.name

            for student in self.students

        ]

        print("\nStudent Names")

        print(names)
        import cProfile


def timer(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        print(f"\nExecution Time : {end-start:.6f} seconds")

        return result

    return wrapper


def log(action):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            print(f"\n[{action}] Operation Started")

            result = func(*args, **kwargs)

            print(f"[{action}] Operation Completed")

            return result

        return wrapper

    return decorator


class ReportWriter:

    def __init__(self, filename: str):

        self.filename = filename

    def __enter__(self):

        self.file = open(self.filename, "w")

        return self.file

    def __exit__(self, exc_type, exc_value, traceback):

        self.file.close()


class StudentManagement(StudentManagement):

    @timer
    @log("SAVE REPORT")
    def save_report(self):

        if len(self.students) == 0:

            print("\nNo Students Found.")

            return

        with ReportWriter("students_report.txt") as file:

            for student in self.students:

                file.write(
                    f"{student.student_id},"
                    f"{student.name},"
                    f"{student.branch},"
                    f"{student.marks}\n"
                )

        print("\nReport Saved Successfully.")

  

    def show_passing_students(self):

        print("\nPassing Students")

        print("-" * 30)

        found = False

        for student in self.passing_students():

            print(student.name)

            found = True

        if not found:

            print("No Student Passed.")

    

    def menu(self):

        while True:

            print("\n========== STUDENT RESULT MANAGEMENT ==========")
            print("1. Add Student")
            print("2. Display Students")
            print("3. Search Student")
            print("4. Update Marks")
            print("5. Delete Student")
            print("6. Show Passing Students")
            print("7. Show Topper")
            print("8. Student Names")
            print("9. Save Report")
            print("10. Exit")

            try:

                choice = int(input("\nEnter Choice : "))

                if choice == 1:

                    self.add_student()

                elif choice == 2:

                    self.display_students()

                elif choice == 3:

                    self.search_student()

                elif choice == 4:

                    self.update_marks()

                elif choice == 5:

                    self.delete_student()

                elif choice == 6:

                    self.show_passing_students()

                elif choice == 7:

                    self.show_topper()

                elif choice == 8:

                    self.student_names()

                elif choice == 9:

                    self.save_report()

                

                elif choice == 10:

                    print("\nThank You")

                    break

                else:

                    print("\nInvalid Choice")

            except ValueError:


                print("\nPlease Enter Numbers Only")


def main():

    system = StudentManagement()

    system.menu()


if __name__ == "__main__":

    main()