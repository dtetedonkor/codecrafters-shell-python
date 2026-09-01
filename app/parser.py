import shlex


class Parser:
    # for the parsing of pipe I want to create a list[list]
    """ the list[list] """
    def parse(self, user_in: str) -> dict:
        tokens = self._tokenize(user_in)

        state = {
            # want to add commands list for pipe
            "command": [],
            "stdout": None,
            "stdout_append": False,
            "stderr": None,
            "stderr_append": False,
            "job": False,
            "pipe": False,
        }

        i = 0

        while i < len(tokens):
            token = tokens[i]

            if token in (">", ">>"):
                i = self._parse_stdout(tokens, i, state)

            elif token == "2":
                i = self._parse_stderr(tokens, i, state)

            elif token == "&":
                state["job"] = True

            elif token == "|":
                state["pipe"] = True

            else:
                state["command"].append(token)

            i += 1

        return state

    def _tokenize(self, user_in: str) -> list[str]:
        user_in = user_in.replace("1>", ">")

        lexer = shlex.shlex(
            user_in,
            posix=True,
            punctuation_chars=">"
        )

        lexer.whitespace_split = True
        lexer.quotes = "'\""
        lexer.escape = "\\"

        return list(lexer)

    def _parse_stdout(self, tokens: list[str], i: int, state: dict) -> int:
        operator = tokens[i]

        if i + 1 < len(tokens):
            state["stdout"] = tokens[i + 1]
            state["stdout_append"] = operator == ">>"
            return i + 1

        return i

    def _parse_stderr(self, tokens: list[str], i: int, state: dict) -> int:
        if i + 1 >= len(tokens):
            state["command"].append(tokens[i])
            return i

        operator = tokens[i + 1]

        if operator not in (">", ">>"):
            state["command"].append(tokens[i])
            return i

        if i + 2 < len(tokens):
            state["stderr"] = tokens[i + 2]
            state["stderr_append"] = operator == ">>"
            return i + 2

        return i + 1

