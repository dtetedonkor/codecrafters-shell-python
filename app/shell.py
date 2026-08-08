import sys
import shutil
import subprocess
import os

class Shell:
    def __init__(self):
        self.builtin = {
            "cd": self._cd,
            "echo": self._echo,
            "pwd": self._pwd,
            "type": self._type,
            "exit": self._exit,
        }

    def run_program(self, command_list: list) -> None:
        """Run an external program."""
        program = shutil.which(command_list[0])

        if program:
            result = subprocess.run(
                command_list,
                capture_output=True,
                text=True,
            )

            sys.stdout.write(result.stdout)
            sys.stderr.write(result.stderr)

        else:
            print(f"{command_list[0]}: command not found")

    def execute(self, command_list: list) -> None:
        if not command_list:
            return

        command = command_list[0]
        args = command_list[1:]

        builtin = self.builtin.get(command)

        if builtin:
            builtin(args)
        else:
            self.run_program(command_list)

    def _exit(self, args: list) -> None:
        sys.exit(0)

    def _cd(self, args: list) -> None:
        if not args:
            path = os.path.expanduser("~")
        else:
            path = os.path.expanduser(args[0])

        try:
            os.chdir(path)
        except OSError:
            print(f"cd: {path}: No such file or directory")

    def _echo(self, args: list) -> None:
        print(" ".join(args))

    def _pwd(self, args: list) -> None:
        print(os.getcwd())

    def _type(self, args: list) -> None:
        if not args:
            return

        cmd = args[0]

        if cmd in self.builtin:
            print(f"{cmd} is a shell builtin")

        else:
            prog = shutil.which(cmd)

            if prog:
                print(prog)
            else:
                print(f"{cmd}: not found")
