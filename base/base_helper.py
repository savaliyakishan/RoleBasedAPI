# Other
import re

class GlobalHelperFunction:
    Response = False
    def validations(self):
        for Key, Value in self.value_list.items():
            valid = False if Value in ["", None, 'null'] else True
            if not valid:
                self.key = Key
                self.Response = True
                break

def validate_password(password):
    regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,}$'
    return bool(re.match(regex, password))

def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return bool(re.match(regex, email))
