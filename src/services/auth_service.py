import hashlib
from datetime import datetime

class AuthService:
    def __init__(self, mysql_repo):
        self.mysql_repo = mysql_repo

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, email, password):
        password_hash = self.hash_password(password)
        created_at = datetime.now()
        return self.mysql_repo.register_user(username, email, password_hash, created_at)
