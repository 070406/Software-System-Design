# Software System Design: Architecture and Scalability (SARS)

## Task 2.1(a) Functional and Non-Functional Requirements

### Functional Requirements

1. Students should be able to log in securely using their credentials.
2. Students should be able to view examination marks and enroll in available courses.
3. Administrators should be able to manage students, courses, faculty, and examination records.

### Non-Functional Requirements

| Non-Functional Requirement | Design Principle Addressed | Explanation |
|---------------------------|----------------------------|-------------|
| System should support 50,000 concurrent users. | Scalability | The application should continue performing efficiently under heavy load. |
| System should remain available during examination result publication. | Availability | Users should be able to access the system even if one server fails. |
| Student information must be protected from unauthorized access. | Security | Authentication, authorization, and encryption should be used to secure sensitive data. |

---

# Task 2.1(b) Monolithic vs Microservices

| Feature | Monolithic Architecture | Microservices Architecture |
|----------|------------------------|----------------------------|
| Independent Deployment | Entire application must be deployed together. | Each service can be deployed independently. |
| Fault Isolation | Failure in one module may crash the whole application. | Failure of one service usually does not affect other services. |
| Management Complexity | Easier to develop and deploy initially. | More complex because multiple services must be managed and monitored. |

### Recommendation

For SARS, a **Microservices Architecture** is recommended because the system must support approximately **50,000 concurrent users** during examination result publication. Independent deployment allows individual services such as Authentication, Student Portal, and Admin Panel to be updated without affecting the rest of the application. Fault isolation ensures that if one service fails, the remaining services continue functioning. Although microservices introduce higher management complexity, they provide significantly better scalability and reliability for a large-scale university application.

---

# Task 2.2(a) High-Level Architecture

## Main Components

### 1. Authentication Service

**Responsibility**

- User login
- User logout
- Password verification
- Authentication token generation

**Interface**

REST API

---

### 2. Student Portal Service

**Responsibility**

- View examination results
- Course enrollment
- View profile

**Interface**

REST API

---

### 3. Admin Panel Service

**Responsibility**

- Manage students
- Manage courses
- Manage faculty
- Update examination marks

**Interface**

REST API

---

### 4. Database Service

**Responsibility**

Store all application data.

**Interface**

SQL Database Query Interface

---

### 5. Email Notification Service

**Responsibility**

Send notifications to students.

**Interface**

REST API

---

### 6. Audit Log Service

**Responsibility**

Maintain activity logs for security and auditing.

**Interface**

REST API

---

# Task 2.2(b) Layered Architecture (Student Portal)

## 1. Presentation Layer

### Responsibilities

- Displays webpages
- Accepts user input
- Shows marks and enrollment status

### Receives

User requests from browser.

### Passes

Validated requests to Business Layer.

---

## 2. Business Layer

### Responsibilities

- Validate business rules
- Check course availability
- Calculate results if required
- Authenticate requests

### Receives

Validated requests from Presentation Layer.

### Passes

Database requests to Data Access Layer.

---

## 3. Data Access Layer

### Responsibilities

- Execute SQL queries
- Read student information
- Save enrollment records
- Retrieve examination marks

### Receives

Database requests from Business Layer.

### Passes

Query results back to Business Layer.

---

# Task 2.2(c) Scaling Strategy

### Scaling Method

Horizontal Scaling

### Reason

Instead of increasing the power of one server, multiple web servers are added. This allows the application to serve many more users simultaneously and provides better fault tolerance.

### Load Balancer

A load balancer distributes incoming requests among available servers.

### Load Balancing Algorithm

**Round Robin**

### Why Round Robin?

Round Robin distributes requests equally across all available servers. Since student requests during result publication are generally similar in size, this algorithm provides a simple and effective distribution of workload.

---

# Task 2.2(d) Elasticity

Elasticity allows the cloud platform to automatically increase or decrease computing resources according to demand.

### During Examination Result Publication

- Additional web servers are automatically added.
- More CPU and memory are allocated.
- System performance remains stable.

### During Semester Break

- Extra servers are automatically removed.
- Only a few servers remain active.
- Infrastructure costs are reduced because unused resources are not running.

Therefore, elasticity improves both performance and cost efficiency.

---

# Task 2.2(e) Session Management Problem

## Problem Name

**Session Affinity (Sticky Session) Problem**

### Problem Description

Suppose a student logs in and the request is handled by **Server A**.

The session information is stored only in Server A's memory.

The next request is sent to **Server B** by the load balancer.

Server B does not contain the student's session.

The student appears to be logged out or receives an authentication error.

---

## Solution 1: Sticky Sessions

The load balancer always routes requests from the same user to the same web server.

### Trade-off

If the selected server crashes, the user's session is lost.

Load distribution may also become uneven because some servers receive more returning users than others.

---

## Solution 2: Centralized Session Storage

Instead of storing sessions inside each web server, sessions are stored in a shared session database or distributed cache.

All web servers access the same session store.

### Trade-off

An additional infrastructure component is required, increasing operational cost and system complexity. If the shared session store becomes unavailable, session retrieval may fail unless it is also made highly available.

---

# Conclusion

The proposed SARS architecture uses microservices, horizontal scaling, load balancing, layered architecture, and centralized session management to support approximately **50,000 concurrent users** efficiently. These design choices improve scalability, reliability, availability, and maintainability while reducing downtime during peak examination periods.
