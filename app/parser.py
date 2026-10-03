import shlex
import re
from .declare import Declare


class Parser:
    def __init__(self, declare=None):
        # Share the same dict object as Declare so new variables are visible here.
        # Declare must only mutate it (self.vars[name] = value), never reassign it.
        self.vars = declare.vars if declare is not None else {}

    def expand(self, token: str) -> str:
        def repl(m):
            name = m.group(1) or m.group(2)       # ${name} or $name
            return str(self.vars.get(name, ""))   # unset vars -> empty string

        return re.sub(r"\$(?:\{(\w+)\}|(\w+))", repl, token)

    def parse(self, user_in: str) -> dict:
        tokens = self._tokenize(user_in)

        state = {
            "command": [],
            "pipe_commands": [],
            "stdout": None,
            "stdout_append": False,
            "stderr": None,
            "stderr_append": False,
            "job": False,
            "pipe": False,
        }

        i = 0

        while i < len(tokens):
            raw = tokens[i]

            # Operators are recognised on the raw token, before expansion
            if raw in (">", ">>"):
                i = self._parse_stdout(tokens, i, state)

            elif raw == "2":
                i = self._parse_stderr(tokens, i, state)

            elif raw == "&":
                state["job"] = True

            elif raw == "|":
                state["pipe"] = True
                state["pipe_commands"].append(state["command"])
                state["command"] = []

            else:
                token = self.expand(raw)
                # Unset variable expanded to nothing: pass no arg at all
                if token != "":
                    state["command"].append(token)

            i += 1

        if state["pipe"] and state["command"]:
            state["pipe_commands"].append(state["command"])
            state["command"] = []

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
            state["stdout"] = self.expand(tokens[i + 1])   # allow $VAR in filenames
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
            state["stderr"] = self.expand(tokens[i + 2])   # allow $VAR in filenames
            state["stderr_append"] = operator == ">>"
            return i + 2

        return i + 1