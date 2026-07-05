# Software System Design

## Architecture Decisions

The SARS application follows a Microservices Architecture.

The major services are:

- Authentication Service
- Student Portal Service
- Admin Panel Service
- Email Notification Service
- Audit Log Service
- Database Service

Microservices were selected because they support independent deployment, better scalability, and fault isolation. This architecture is suitable for handling approximately 50,000 concurrent users during examination result publication.

---

# SOLID Principles

## Single Responsibility Principle (SRP)

The Student class only stores student information and related operations. It does not send emails or perform database operations.

---

## Open/Closed Principle (OCP)

The Enrollment class can be extended by creating subclasses such as WaitlistedEnrollment without modifying the original Enrollment class.

---

## Dependency Inversion Principle (DIP)

The Enrollment class depends on the EnrollmentRepository interface instead of a concrete database implementation. This allows different repository implementations (e.g., MySQL, PostgreSQL, or in-memory storage) without changing business logic.

---

# Observer Pattern

The Observer pattern keeps the Admin Panel loosely coupled from notification services.

Whenever student marks are updated:

- The Admin Panel notifies the MarksUpdateNotifier.
- The notifier informs all registered observers.
- EmailNotifier sends an email.
- AuditLogNotifier records the update.

New notification services can be added without changing the Admin Panel code.

---

# Redundancy Strategy

To achieve high availability, the database is replicated using a primary-replica configuration.

If the primary database server fails:

- The replica is promoted to become the new primary.
- Read requests continue from the promoted replica.
- Write requests are redirected to the new primary.

Replication minimizes downtime and reduces the risk of data loss.

---

# Fault Isolation

In the Microservices Architecture, each service runs independently.

If the Email Notification Service fails:

- Students can still view marks.
- Students can still enroll in courses.
- Only email notifications are unavailable.

The Student Portal should catch exceptions from the email call, log the error, and continue processing the main request so that failures in the notification path do not interrupt marks display or enrollment.

---

# Replication Trade-Off

Synchronous replication increases write latency because the primary waits for the replica to acknowledge each write before confirming success to the application.

Asynchronous replication provides faster writes but can result in replica lag.

If the primary crashes before the latest transaction reaches the replica:

1. The replica contains only the last fully replicated and consistent data.
2. Students reading from the promoted replica see that last consistent state; the newest transaction may be missing.
3. The database administrator should recover any missing transactions from the primary's write-ahead log (WAL) or binary log if available. If recovery is not possible, the administrator must accept the small data loss and promote the replica at the last known consistent state before declaring the system fully consistent.
