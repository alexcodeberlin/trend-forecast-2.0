# Prompt for Advanced Infrastructure Security Implementation (Phase 2)

You are an Infrastructure and Security Engineer. Your task is to implement the infrastructure-heavy components of the "Whole Secure Pipeline" for the existing project.

## Current State
The application has a professional Repository/Service pattern, uses environment variables, Argon2id for hashing, and has PII masking and audit logging implemented in the code.

## Your Task
Implement the following infrastructure enhancements:

### 1. Secrets Vaulting (Phase 1)
- **Objective**: Replace `.env` disk storage with a Secrets Manager.
- **Action**: 
    - Setup a local **HashiCorp Vault** instance (or a mock service for development).
    - Refactor `src/config/settings.py` to authenticate with the Vault and fetch `TWITTER_BEARER_TOKEN` and database passwords into memory at runtime.
    - Ensure secrets are never logged or written to disk.

### 2. mTLS + TLS 1.3 (Phase 2)
- **Objective**: Enforce mutual authentication for database connections.
- **Action**:
    - Generate a internal CA, server certificates, and client certificates.
    - Configure the **MySQL** and **Elasticsearch** repositories to provide the Client Certificate and Key during connection.
    - Update `Settings` to manage paths to these certificates.

### 3. Secure Storage (Data at Rest) (Phase 3)
- **Objective**: Encrypt physical storage files.
- **Action**:
    - **Elasticsearch**: Enable settings for AES-256 Transparent Data Encryption (TDE).
    - **MySQL**: Enable InnoDB Tablespace Encryption.
    - **SQLite**: Replace the standard `sqlite3` library with `pysqlcipher3` (SQLCipher) and refactor `SQLiteRepository` to provide a passphrase for opening the `.db` file.

### 4. Network Isolation (VPC simulation) (Phase 2)
- **Objective**: Hide databases from public access.
- **Action**:
    - Use **Docker Compose** to create a private network.
    - Place MySQL and Elasticsearch in the private network with NO exposed ports to the host.
    - Place the Python App in the same network so it can communicate with them internally.

## Success Criteria
- The app can fetch data and save it without any `.env` file present (using Vault).
- Database connections fail if the client certificate is missing (mTLS).
- The `.db` file is unreadable by standard SQLite browsers (SQLCipher).
- No database ports are accessible from outside the Docker network.
