import shlex


class Parser:
    def parse(self, user_in: str) -> dict:
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

        command_state = {
            "command": [],
            "stdout": None,
            "stdout_append": False,
            "stderr": None,
            "stderr_append": False,
            "job": False,
        }

        i = 0

        while i < len(tokens):
            token = tokens[i]

            
            
            # stdout: > or >>
            if token == ">>":
                i += 1

                if i < len(tokens):
                    command_state["stdout"] = tokens[i]
                    command_state["stdout_append"] = True
            elif token == "&":
                            command_state["job"] =  True
            elif token == ">":
                i += 1

                if i < len(tokens):
                    command_state["stdout"] = tokens[i]
                    command_state["stdout_append"] = False

            # stderr: 2> or 2>>
            elif token == "2":
                if i + 1 < len(tokens) and tokens[i + 1] == ">>":
                    i += 2

                    if i < len(tokens):
                        command_state["stderr"] = tokens[i]
                        command_state["stderr_append"] = True

                elif i + 1 < len(tokens) and tokens[i + 1] == ">":
                    i += 2

                    if i < len(tokens):
                        command_state["stderr"] = tokens[i]
                        command_state["stderr_append"] = False

                else:
                    command_state["command"].append(token)

            else:
                command_state["command"].append(token)

            i += 1

        return command_state