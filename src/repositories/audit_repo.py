import logging
import os
from datetime import datetime

class AuditRepository:
    def __init__(self, log_file="audit.log"):
        self.logger = logging.getLogger("AuditLogger")
        self.logger.setLevel(logging.INFO)
        
        # Create file handler which logs even debug messages
        if not self.logger.handlers:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def log_event(self, user, action, status, details=""):
        message = f"User: {user} | Action: {action} | Status: {status} | Details: {details}"
        self.logger.info(message)
        print(f"🔒 [AUDIT] {message}")
