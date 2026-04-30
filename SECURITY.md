# Security Architecture and Features

This document outlines the security measures implemented in this project for the Software Engineering Security Module.

## 1. CIA Triad Implementation

### Confidentiality
- **Environment Variables**: Sensitive credentials (API tokens, database passwords) are managed via a `.env` file and never hardcoded in the source code.
- **TLS/SSL Encryption**: All data in transit between the application and external databases (Elasticsearch and MySQL) is protected using TLS/SSL encryption.
- **Support for mTLS**: The architecture is designed to support Mutual TLS (mTLS), requiring client certificates for database access.

### Integrity
- **Parameterized Queries**: To prevent SQL and NoSQL injection, all database interactions use parameterized queries or high-level ORM methods (Elasticsearch-DSL).
- **Input Cleaning**: Data from the Twitter API is sanitized and cleaned before processing and storage.

### Availability
- **Rate Limit Handling**: The Twitter repository includes logic to respect API rate limits and handle `TooManyRequests` errors gracefully.
- **Robust Error Handling**: Connection failures to databases are caught and reported without crashing the entire application.

## 2. Professional OOP Architecture

The project uses a **Repository-Service Pattern** which improves security through **Separation of Concerns**:
- **Repositories**: Encapsulate all data access logic.
- **Services**: Encapsulate business logic and security processing (like password hashing).
- **Decoupling**: The UI (Streamlit) is completely decoupled from the security-sensitive data layer.

## 3. User Authentication Security
- **Secure Authentication**: A fully functional login system implemented in `AuthService` with **Argon2id** verification.
- **Session Management**: Secure state management via `st.session_state` to track authenticated users.
- **Detailed Audit Logging**: Every login attempt (success, failure, or incorrect password) is recorded in `audit.log`.

## 4. Threat Model (STRIDE)
- **Spoofing**: Mitigated by mTLS and strong authentication.
- **Tampering**: Protected by TLS encryption and parameterized queries.
- **Information Disclosure**: Prevented by moving secrets out of the code and into the environment.
- **Elevation of Privilege**: Handled by implementing the Principle of Least Privilege in database user roles.
