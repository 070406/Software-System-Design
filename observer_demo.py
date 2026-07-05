"""
=========================================================
observer_demo.py

Task 2.3(d)

Observer Design Pattern

=========================================================
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------
# Observer Interface
# ---------------------------------------------------------

class Observer(ABC):

    @abstractmethod
    def update(self, student_id: int, new_marks: float):
        pass


# ---------------------------------------------------------
# Email Notification Service
# ---------------------------------------------------------

class EmailNotifier(Observer):

    def update(self, student_id: int, new_marks: float):

        print("--------------------------------")

        print("Email Notification Service")

        print(
            f"Email sent to Student {student_id}"
        )

        print(
            f"Updated Marks = {new_marks}"
        )


# ---------------------------------------------------------
# Audit Log Service
# ---------------------------------------------------------

class AuditLogNotifier(Observer):

    def update(self, student_id: int, new_marks: float):

        print("--------------------------------")

        print("Audit Log Service")

        print(
            f"Student {student_id} marks updated."
        )

        print(
            f"New Marks = {new_marks}"
        )


# ---------------------------------------------------------
# Subject
# ---------------------------------------------------------

class MarksUpdateNotifier:

    def __init__(self):

        self.observers = []


    # Register observer
    def register(self, observer: Observer):

        self.observers.append(observer)


    # Remove observer
    def deregister(self, observer: Observer):

        self.observers.remove(observer)


    # Notify all observers
    def notify(self, student_id, new_marks):

        for observer in self.observers:

            observer.update(student_id, new_marks)


    # Admin updates marks
    def update_marks(self, student_id, new_marks):

        print()

        print("==============================")

        print("Admin Panel")

        print(
            f"Student {student_id} marks updated to {new_marks}"
        )

        print("==============================")

        self.notify(student_id, new_marks)


# ---------------------------------------------------------
# Demonstration
# ---------------------------------------------------------

if __name__ == "__main__":

    notifier = MarksUpdateNotifier()

    email_service = EmailNotifier()

    audit_service = AuditLogNotifier()

    # Register observers

    notifier.register(email_service)

    notifier.register(audit_service)

    # Marks updated

    notifier.update_marks(101, 91)

    print("\nRemoving Email Notification Service...\n")

    # Deregister email service

    notifier.deregister(email_service)

    # Only Audit Log should receive notification

    notifier.update_marks(101, 95)
