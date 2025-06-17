class Session:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._instance.user_id = None
            cls._instance.username = None
        return cls._instance

    def set_user(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def clear(self):
        self.user_id = None
        self.username = None
