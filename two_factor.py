from datetime import datetime, timedelta
import random


class TwoFactorAuth:
    def __init__(self):
        self.active_codes = {}

    def generate_code(self, user_key, minutes_valid=5):
        user_key = str(user_key).strip().lower()
        code = str(random.randint(100000, 999999))
        expires_at = datetime.now() + timedelta(minutes=minutes_valid)

        self.active_codes[user_key] = {
            "code": code,
            "expires_at": expires_at
        }

        return code

    def verify_code(self, user_key, entered_code):
        user_key = str(user_key).strip().lower()

        if user_key not in self.active_codes:
            return False

        saved_info = self.active_codes[user_key]

        if datetime.now() > saved_info["expires_at"]:
            del self.active_codes[user_key]
            return False

        if str(entered_code).strip() == saved_info["code"]:
            del self.active_codes[user_key]
            return True

        return False

    def clear_code(self, user_key):
        user_key = str(user_key).strip().lower()

        if user_key in self.active_codes:
            del self.active_codes[user_key]