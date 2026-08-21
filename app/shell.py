import os
import readline
import shutil
import subprocess
import sys
from pathlib import Path


class Shell:
    def __init__(self):
        self.builtin = {
            "cd": self._cd,
            "echo": self._echo,
            "pwd": self._pwd,
            "type": self._type,
            "exit": self._exit,
            "complete": self._complete,
        }
        self.BUILTIN = ["cd", "pwd", "type", "exit", "echo", "complete"]
        self.completions = {}

    def get_posix_executables(self) -> set[str]:
        path_dirs = os.get_exec_path()
        executable_files = set()

        for dir_str in path_dirs:
            path_obj = Path(dir_str)

            if not path_obj.is_dir():
                continue

            try:
                for child in path_obj.iterdir():
                    if child.is_file() and os.access(child, os.X_OK):
                        executable_files.add(child.name)

            except PermissionError:
                continue

        return sorted(executable_files)

    def get_dir_files(self, path=".") -> set[str]:
        """Return a set of filenames for all files (not directories) in the given path."""
        return {f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))}

    def get_dir(self, path="."):
        return {f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))}

    def completer(self, text: str, state: int):
        COMP_LINE = readline.get_line_buffer()
        last_str = COMP_LINE.rsplit(" ", 1)[-1]
        parts = COMP_LINE.split()

        COMP_POINT = len(COMP_LINE.encode('utf-8'))

        # Nothing has been typed yet
        if not parts:
            return None

        command = parts[0]

        # -----------------------------------
        # Custom completion: complete -C
        # -----------------------------------
        if command in self.completions:
            script = self.completions[command]

            # Example:
            # git remote <TAB>
            #
            # parts = ["git", "remote"]
            # current_word = ""
            # previous_word = "remote"
            if COMP_LINE.endswith(" "):
                current_word = ""

                if len(parts) >= 2:
                    previous_word = parts[-1]
                else:
                    previous_word = ""

            # Example:
            # git remote set<TAB>
            #
            # parts = ["git", "remote", "set"]
            # current_word = "set"
            # previous_word = "remote"
            else:
                current_word = parts[-1]

                if len(parts) >= 2:
                    previous_word = parts[-2]
                else:
                    previous_word = ""

            process_obj = subprocess.run(
                [script, command, current_word, previous_word,COMP_LINE,COMP_POINT],
                capture_output=True,
                text=True,
                check=True
            )

            completion = process_obj.stdout

            candidates = set(completion.splitlines())

            options = sorted(
                entry for entry in candidates if entry.startswith(current_word)
            )

            # No completion candidates
            if not options:
                if state == 0:
                    print("\x07", end="", flush=True)

                return None

            if state >= len(options):
                return None

            clean_comp = options[state].rstrip()
            return clean_comp + " "

        # -----------------------------------
        # Completing a path
        # -----------------------------------
        if "/" in last_str:
            path, prefix = last_str.rsplit("/", 1)

            entries = self.get_dir(path)
            entries.update(self.get_dir_files(path))

            options = sorted(entry for entry in entries if entry.startswith(prefix))

            if state >= len(options):
                return None

            entry = options[state]
            full_path = os.path.join(path, entry)

            if os.path.isdir(full_path):
                return entry + "/"

            return entry + " "

        # -----------------------------------
        # Completing a filename/directory
        # -----------------------------------
        if " " in COMP_LINE:
            entries = self.get_dir()
            entries.update(self.get_dir_files())

            options = sorted(entry for entry in entries if entry.startswith(last_str))

            if state >= len(options):
                return None

            entry = options[state]

            if os.path.isdir(entry):
                return entry + "/"

            return entry + " "

        # -----------------------------------
        # Completing commands
        # -----------------------------------
        exec_list = self.get_posix_executables()

        commands = set(self.BUILTIN)
        commands.update(exec_list)

        options = sorted(command for command in commands if command.startswith(text))

        if state >= len(options):
            return None

        return options[state] + " "

    def run_program(
        self,
        command_list: list,
        stdout=None,
        stderr=None,
        stdout_append=False,
        stderr_append=False,
    ) -> None:

        program = shutil.which(command_list[0])
        os.get_exec_path()
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
            # stdout
            if isinstance(stdout, str):
                mode = "a" if stdout_append else "w"
                stdout_file = open(stdout, mode)
                stdout_dest = stdout_file
            else:
                stdout_dest = stdout

            # stderr
            if isinstance(stderr, str):
                mode = "a" if stderr_append else "w"
                stderr_file = open(stderr, mode)
                stderr_dest = stderr_file
            else:
                stderr_dest = stderr

            subprocess.run(
                command_list,
                text=True,
                stdout=stdout_dest,
                stderr=stderr_dest,
                check=True
            )

        finally:
            if stdout_file:
                stdout_file.close()

            if stderr_file:
                stderr_file.close()

    def execute(self, parsed: dict) -> None:
        """execute is the central funcntion that calls bulitins or
        executable functions to print to shell output.
        It doesnt perform any actions just acts as forwarder.
         It also manages redirects to standard stdout or stderr for
          both builtin commands and executables"""

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
            stdout_file = None
            stderr_file = None

            try:
                # stdout
                if stdout:
                    mode = "a" if stdout_append else "w"
                    stdout_file = open(stdout, mode)
                    stdout_dest = stdout_file
                else:
                    stdout_dest = sys.stdout

                # stderr
                if stderr:
                    mode = "a" if stderr_append else "w"
                    stderr_file = open(stderr, mode)
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
            self.run_program(command_list, stdout, stderr, stdout_append, stderr_append)

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
