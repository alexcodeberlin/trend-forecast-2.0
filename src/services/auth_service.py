from argon2 import PasswordHasher, exceptions
from datetime import datetime
import re
from src.repositories.audit_repo import AuditRepository

class AuthService:
    def __init__(self, mysql_repo):
        self.mysql_repo = mysql_repo
        self.ph = PasswordHasher()
        self.audit_repo = AuditRepository()

    def hash_password(self, password):
        return self.ph.hash(password)

    def is_valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def register(self, username, email, password):
        if not username or not email or not password:
            return False, "All fields are required."
        
        if not self.is_valid_email(email):
            self.audit_repo.log_event(username, "REGISTER", "FAILURE", f"Invalid email: {email}")
            return False, "Invalid email format."

        if len(password) < 8:
            self.audit_repo.log_event(username, "REGISTER", "FAILURE", "Password too short")
            return False, "Password must be at least 8 characters long."
        
        password_hash = self.hash_password(password)
        created_at = datetime.now()
        success, message = self.mysql_repo.register_user(username, email, password_hash, created_at)
        
        status = "SUCCESS" if success else "FAILURE"
        self.audit_repo.log_event(username, "REGISTER", status, message)
        
        return success, message

    def login(self, username, password):
        if not username or not password:
            return False, "Username and password are required."

        user_data = self.mysql_repo.get_user_by_username(username)
        
        if not user_data:
            self.audit_repo.log_event(username, "LOGIN", "FAILURE", "User not found")
            return False, "Invalid username or password."

        try:
            # Verify the hash using Argon2
            self.ph.verify(user_data['password_hash'], password)
            
            # Check if hash needs re-hashing (security best practice)
            if self.ph.check_needs_rehash(user_data['password_hash']):
                new_hash = self.hash_password(password)
                # In a real app, you'd update the DB here
                pass

            self.audit_repo.log_event(username, "LOGIN", "SUCCESS", "User authenticated")
            return True, "Login successful!"
        
        except exceptions.VerifyMismatchError:
            self.audit_repo.log_event(username, "LOGIN", "FAILURE", "Incorrect password")
            return False, "Invalid username or password."
        except Exception as e:
            self.audit_repo.log_event(username, "LOGIN", "ERROR", str(e))
            return False, "An error occurred during login."
