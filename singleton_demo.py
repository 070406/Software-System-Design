"""
=========================================================
singleton_demo.py

Task 2.3(c)

Thread-Safe Singleton Design Pattern

Language: Python
=========================================================
"""

import threading


class DatabaseConnection:
    """
    Singleton class.

    Only ONE object of this class can exist
    throughout the application.
    """

    # Stores the singleton instance
    _instance = None

    # Lock used for thread safety
    _lock = threading.Lock()

    def __init__(self):
        """
        Constructor.

        Normally this would establish a real
        database connection.
        """
        print("Database connection established.")

        self.connection = "Connected to University Database"

    @classmethod
    def get_connection(cls):
        """
        Returns the singleton object.

        Thread-safe implementation using
        double-checked locking.
        """

        # First check (avoids locking every time)
        if cls._instance is None:

            # Only one thread can enter here
            with cls._lock:

                # Second check
                if cls._instance is None:
                    cls._instance = cls()

        return cls._instance


# ---------------------------------------------------------
# Demonstration
# ---------------------------------------------------------

def worker():

    db = DatabaseConnection.get_connection()

    print(
        f"Thread: {threading.current_thread().name}"
    )

    print(
        f"Object ID: {id(db)}"
    )

    print(db.connection)

    print()


if __name__ == "__main__":

    threads = []

    # Create five concurrent threads
    for i in range(5):

        thread = threading.Thread(
            target=worker,
            name=f"Thread-{i+1}"
        )

        threads.append(thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads
    for thread in threads:
        thread.join()


"""
---------------------------------------------------------

Explanation

Naive lazy initialization:

if instance is None:
    instance = DatabaseConnection()

is NOT thread-safe.

Suppose two threads execute this code
at exactly the same time.

Both see that instance is None.

Both create a new object.

Result:

Two DatabaseConnection objects exist,
violating the Singleton pattern.

Using threading.Lock() ensures that only
one thread creates the object while all
other threads wait.

The second check inside the lock
(double-checked locking) prevents creating
multiple objects even under concurrent access.

---------------------------------------------------------
"""
