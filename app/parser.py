import shlex


class _Parser:
    def parse(self, user_in: str):
        lexer = shlex.shlex(user_in, posix=True)

        lexer.whitespace_split = True

        lexer.quotes = "'\""

        lexer.escape = "\\"

        return list(lexer)