import os
import readline
import shutil
import subprocess
import sys
from contextlib import ExitStack



class Shell:
    def __init__(self, completer=None):
        self.builtin = {
            "cd": self._cd,
            "echo": self._echo,
            "pwd": self._pwd,
            "type": self._type,
            "exit": self._exit,
            "complete": self._complete,
        }
        # Share the same dict readline's Completer reads from, so `complete -C`
        # registrations made here are actually visible during tab-completion.
        self.completions = completer.completions if completer is not None else {}

    def run_program(
        self,
        command_list: list,
        stdout=None,
        stderr=None,
        stdout_append=False,
        stderr_append=False,
    ) -> None:

        program = shutil.which(command_list[0])
        if not command_list:
            return

        # Program doesn't exist print it doesnt exit
        if not program:
            print(f"{command_list[0]}: command not found")
            return

        if stdout is None:
            stdout = sys.stdout

        if stderr is None:
            stderr = sys.stderr

        try:
            with ExitStack() as stack:
                # stdout redirection
                if isinstance(stdout, str):
                    mode = "a" if stdout_append else "w"

                    stdout_dest = stack.enter_context(open(stdout, mode))
                else:
                    stdout_dest = stdout

                # stderr redirection
                if isinstance(stderr, str):
                    mode = "a" if stderr_append else "w"

                    stderr_dest = stack.enter_context(open(stderr, mode))
                else:
                    stderr_dest = stderr

                subprocess.run(
                    command_list, text=True, stdout=stdout_dest, stderr=stderr_dest,check=True
                )

        except FileNotFoundError:
            # Executable couldn't be found.
            # Return to the shell loop without printing anything.
            return

        except subprocess.CalledProcessError:
            return

   

    def execute(self, parsed: dict) -> None:
        """Execute builtin commands or external programs.

        Handles stdout/stderr redirection for both builtin commands
        and external programs.
        """

        command_list = parsed["command"]
        stdout = parsed["stdout"]
        stderr = parsed["stderr"]
        stdout_append = parsed["stdout_append"]
        stderr_append = parsed["stderr_append"]

        if not command_list:
            return

        command = command_list[0]
        args = command_list[1:]

        builtin = self.builtin.get(command)

        if builtin:
            with ExitStack() as stack:

                # stdout
                if stdout:
                    mode = "a" if stdout_append else "w"
                    stdout_dest = stack.enter_context(
                        open(stdout, mode)
                    )
                else:
                    stdout_dest = sys.stdout

                # stderr
                if stderr:
                    mode = "a" if stderr_append else "w"
                    stderr_dest = stack.enter_context(
                        open(stderr, mode)
                    )
                else:
                    stderr_dest = sys.stderr

                builtin(args, stdout_dest, stderr_dest)

        else:
            self.run_program(
                command_list,
                stdout,
                stderr,
                stdout_append,
                stderr_append
            )

    def _exit(self, args, stdout=sys.stdout, stderr=sys.stderr) -> None:
        sys.exit(0)

    def _cd(self, args, stdout=sys.stdout, stderr=sys.stderr) -> None:

        if not args:
            path = os.path.expanduser("~")
        else:
            path = os.path.expanduser(args[0])

        try:
            os.chdir(path)

        except OSError:
            stderr.write(f"cd: {path}: No such file or directory\n")

    def _echo(self, args, stdout=sys.stdout, stderr=sys.stderr):
        stdout.write(" ".join(args) + "\n")

    def _pwd(self, args, stdout=sys.stdout, stderr=sys.stderr) -> None:
        stdout.write(os.getcwd() + "\n")

    def _complete(self, args, stdout=sys.stdout, stderr=sys.stderr):
        command = ""
        path = ""
        flag = args[0]
        if flag == "-p":
            command = args[1]
            if command in self.completions:
                print(f"complete -C '{self.completions[command]}' {command}")
            else:
                print(f"complete: {command}: no completion specification")
        elif flag == "-C":
            path = args[1]
            command = args[2]
            self.completions[command] = path
        elif flag == "-r":
             command = args[1]
             self.completions.pop(command,None)

    def _type(self, args, stdout=sys.stdout, stderr=sys.stderr) -> None:

        if not args:
            return

        cmd = args[0]

        if cmd in self.builtin:
            stdout.write(f"{cmd} is a shell builtin\n")

        else:
            prog = shutil.which(cmd)

            if prog:
                stdout.write(prog + "\n")
            else:
                stdout.write(f"{cmd}: not found\n")