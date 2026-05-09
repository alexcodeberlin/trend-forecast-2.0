from datetime import datetime

class AuthService:
    def __init__(self, mysql_repo):
        self.mysql_repo = mysql_repo

    def register(self, username, email, password):
        print(f"🛠️ AuthService: Registering user '{username}'...")
        # (Security hashing to be added later as requested)
        return self.mysql_repo.register_user(username, email, password, datetime.now())

    def login(self, username, password):
        print(f"🛠️ AuthService: Attempting login for user '{username}'...")
        user = self.mysql_repo.get_user_by_username(username)
        if user and user['password_hash'] == password:
            print(f"✅ Login success for '{username}'")
            return True, "Login successful!"
        else:
            print(f"❌ Login failed for '{username}'")
            return False, "Invalid username or password."
