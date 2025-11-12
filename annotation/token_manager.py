import uuid

class TokenManager:
    def __init__(self):
        self.tokens = {}

    def get(self, name):
        if name not in self.tokens:
            self.tokens[name] = uuid.uuid4().hex
        return self.tokens[name]
