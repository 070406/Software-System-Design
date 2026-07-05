"""
=========================================================
lld_classes.py
Task 2.3(a) & 2.3(b)

Student Class
Enrollment Class
EnrollmentRepository Interface

SOLID Principles Applied:
- Single Responsibility Principle (SRP)
- Open/Closed Principle (OCP)
- Dependency Inversion Principle (DIP)
=========================================================
"""

from abc import ABC, abstractmethod


# -------------------------------------------------------
# Student Class
# -------------------------------------------------------

class Student:
    """
    SRP:
    Student class only manages student information.
    It does NOT send emails or perform database operations.
    """

    def __init__(
        self,
        student_id: int,
        student_name: str,
        department: str,
        email: str
    ):
        self.student_id = student_id
        self.student_name = student_name
        self.department = department
        self.email = email

    def enroll_course(self, course_code: str) -> str:
        return f"{self.student_name} enrolled in {course_code}"

    def view_marks(self) -> str:
        return f"Displaying marks for {self.student_name}"

    def update_profile(
        self,
        new_email: str
    ) -> None:
        self.email = new_email


# -------------------------------------------------------
# Enrollment Base Class
# -------------------------------------------------------

class Enrollment:
    """
    OCP:
    This class is open for extension.
    New enrollment types can inherit from it
    without modifying this class.
    """

    def __init__(
        self,
        student_id: int,
        course_code: str,
        marks: float
    ):
        self.student_id = student_id
        self.course_code = course_code
        self.marks = marks

    def calculate_grade(self) -> str:

        if self.marks >= 90:
            return "A"

        elif self.marks >= 75:
            return "B"

        elif self.marks >= 60:
            return "C"

        elif self.marks >= 40:
            return "D"

        else:
            return "F"


# -------------------------------------------------------
# Example Extension
# (Open/Closed Principle)
# -------------------------------------------------------

class WaitlistedEnrollment(Enrollment):

    def __init__(
        self,
        student_id: int,
        course_code: str,
        marks: float,
        position: int
    ):
        super().__init__(
            student_id,
            course_code,
            marks
        )

        self.position = position

    def waitlist_position(self) -> str:
        return f"Current Waitlist Position: {self.position}"


# -------------------------------------------------------
# EnrollmentRepository Interface
# -------------------------------------------------------

class EnrollmentRepository(ABC):
    """
    Dependency Inversion Principle

    Enrollment depends on this abstraction,
    not on a concrete database implementation.
    """

    @abstractmethod
    def save(
        self,
        enrollment: Enrollment
    ) -> None:
        pass

    @abstractmethod
    def find_by_student(
        self,
        student_id: int
    ) -> list:
        pass

    @abstractmethod
    def delete(
        self,
        student_id: int,
        course_code: str
    ) -> None:
        pass

    @abstractmethod
    def update_marks(
        self,
        student_id: int,
        course_code: str,
        marks: float
    ) -> None:
        pass


# -------------------------------------------------------
# Example Repository Implementation
# -------------------------------------------------------

class MemoryEnrollmentRepository(EnrollmentRepository):
    """
    Simple in-memory implementation
    used for demonstration.
    """

    def __init__(self):
        self.records = []

    def save(
        self,
        enrollment: Enrollment
    ) -> None:

        self.records.append(enrollment)

    def find_by_student(
        self,
        student_id: int
    ) -> list:

        return [
            e for e in self.records
            if e.student_id == student_id
        ]

    def delete(
        self,
        student_id: int,
        course_code: str
    ) -> None:

        self.records = [
            e for e in self.records
            if not (
                e.student_id == student_id and
                e.course_code == course_code
            )
        ]

    def update_marks(
        self,
        student_id: int,
        course_code: str,
        marks: float
    ) -> None:

        for e in self.records:

            if (
                e.student_id == student_id and
                e.course_code == course_code
            ):
                e.marks = marks


# -------------------------------------------------------
# Demonstration
# -------------------------------------------------------

if __name__ == "__main__":

    student = Student(
        101,
        "Harshita",
        "Computer Science",
        "harshita@example.com"
    )

    enrollment = Enrollment(
        101,
        "CS101",
        86
    )

    repo = MemoryEnrollmentRepository()

    repo.save(enrollment)

    print(student.enroll_course("CS101"))
    print(student.view_marks())

    print("Grade:", enrollment.calculate_grade())

    print(repo.find_by_student(101))
