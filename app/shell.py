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
     
    def run_program(self, command_list: list, stdout=None, stderr=None) -> None:

        program = shutil.which(command_list[0])

        if not program:
            print(f"{command_list[0]}: command not found")
            return

        if stdout is None:
            stdout = sys.stdout

        if stderr is None:
            stderr = sys.stderr

        stdout_file = None
        stderr_file = None

        try:
            if isinstance(stdout, str):
                stdout_file = open(stdout, "w")
                stdout_dest = stdout_file
            else:
                stdout_dest = stdout

            if isinstance(stderr, str):
                stderr_file = open(stderr, "w")
                stderr_dest = stderr_file
            else:
                stderr_dest = stderr

            subprocess.run(
                command_list,
                text=True,
                stdout=stdout_dest,
                stderr=stderr_dest,
            )

        finally:
            if stdout_file:
                stdout_file.close()

            if stderr_file:
                stderr_file.close()

    def execute(self, parsed: dict) -> None:
        command_list = parsed["command"]
        stdout = parsed["stdout"]
        stderr = parsed["stderr"]

        if not command_list:
            return

        command = command_list[0]
        args = command_list[1:]

        builtin = self.builtin.get(command)

        if builtin:
            stdout_file = None
            stderr_file = None

            try:
                if stdout:
                    stdout_file = open(stdout, "w")
                    stdout_dest = stdout_file
                else:
                    stdout_dest = sys.stdout

                if stderr:
                    stderr_file = open(stderr, "w")
                    stderr_dest = stderr_file
                else:
                    stderr_dest = sys.stderr

                builtin(args, stdout_dest, stderr_dest)

            finally:
                if stdout_file:
                    stdout_file.close()

                if stderr_file:
                    stderr_file.close()

        else:
            self.run_program(
                command_list,
                stdout,
                stderr
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
            print(f"cd: {path}: No such file or directory")

    def _echo(self, args, stdout=sys.stdout, stderr=sys.stderr):
        stdout.write(" ".join(args) + "\n")
    def _pwd(self, args, stdout=sys.stdout, stderr=sys.stderr) -> None:
        print(os.getcwd())

    def _type(self, args, stdout=sys.stdout, stderr=sys.stderr) -> None:
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