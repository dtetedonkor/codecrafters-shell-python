from enum import Enum

class States(Enum):
    UNQUOTED = 1
    SINGLE_QUOTED = 2
    DOUBLE_QUOTED = 3
    BACKSLASH = 4


class _Parser:
    def __init__(self):
        self.state = States.UNQUOTED
        self.current_token = []
        self.tokens = []

    def handle_unquoted(self, char):
        if char == "'":
            self.state = States.SINGLE_QUOTED

        elif char == '"':
            self.state = States.DOUBLE_QUOTED

        elif char == "\\":
            self.state = States.BACKSLASH

        elif char.isspace():
            self.finish_token()

        else:
            self.current_token.append(char)

    def handle_single_quoted(self, char):
        if char == "'":
            self.state = States.UNQUOTED
        else:
            self.current_token.append(char)

    def handle_double_quoted(self, char):
        if char == '"':
            self.state = States.UNQUOTED

        elif char == "\\":
            self.state = States.BACKSLASH

        else:
            self.current_token.append(char)

    def handle_backslash(self, char):
        self.current_token.append(char)
        self.state = States.UNQUOTED

    def finish_token(self):
        if self.current_token:
            self.tokens.append("".join(self.current_token))
            self.current_token = []

    def process_char(self, char):
        if self.state == States.UNQUOTED:
            self.handle_unquoted(char)

        elif self.state == States.SINGLE_QUOTED:
            self.handle_single_quoted(char)

        elif self.state == States.DOUBLE_QUOTED:
            self.handle_double_quoted(char)

        elif self.state == States.BACKSLASH:
            self.handle_backslash(char)

    def parse(self, user_in: str):
        self.state = States.UNQUOTED
        self.current_token = []
        self.tokens = []

        for char in user_in:
            self.process_char(char)

        self.finish_token()

        return self.tokens
