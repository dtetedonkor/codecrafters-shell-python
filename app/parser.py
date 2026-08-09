import shlex


class _Parser:
    def parse(self, user_in: str):
        user_in = user_in.replace("1>", ">")

        lexer = shlex.shlex(
            user_in,
            posix=True,
            punctuation_chars=">"
        )

        lexer.whitespace_split = True
        lexer.quotes = "'\""
        lexer.escape = "\\"

        tokens = list(lexer)

        result = {
            "command": [],
            "stdout": None,
            "stdout_append": False,
            "stderr": None,
            "stderr_append": False
        }

        i = 0

        while i < len(tokens):
            token = tokens[i]

            # stdout: > or >>
            if token == ">>":
                i += 1

                if i < len(tokens):
                    result["stdout"] = tokens[i]
                    result["stdout_append"] = True

            elif token == ">":
                i += 1

                if i < len(tokens):
                    result["stdout"] = tokens[i]
                    result["stdout_append"] = False

            # stderr: 2> or 2>>
            elif token == "2":
                if i + 1 < len(tokens) and tokens[i + 1] == ">>":
                    i += 2

                    if i < len(tokens):
                        result["stderr"] = tokens[i]
                        result["stderr_append"] = True

                elif i + 1 < len(tokens) and tokens[i + 1] == ">":
                    i += 2

                    if i < len(tokens):
                        result["stderr"] = tokens[i]
                        result["stderr_append"] = False

                else:
                    result["command"].append(token)

            else:
                result["command"].append(token)

            i += 1

        return result