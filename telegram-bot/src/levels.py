class LoginLevel:
    def __init__(self) -> None:
        self.waiting_for_username = 0
        self.waiting_for_password = 1

class SignupLevel:
    def __init__(self) -> None:
        self.waiting_for_username = 0
        self.waiting_for_email = 1
        self.waiting_for_password = 2

LOGIN_LEVEL = LoginLevel()
SIGNUP_LEVEL = SignupLevel()

class Login:
    def __init__(self, chat_id) -> None:
        self.chat_id = chat_id
        self.username = ''
        self.password = ''
        self.level = LOGIN_LEVEL.waiting_for_username

class Signup:
    def __init__(self, chat_id) -> None:
        self.chat_id = chat_id
        self.username = ''
        self.email = ''
        self.password = ''
        self.level = SIGNUP_LEVEL.waiting_for_username