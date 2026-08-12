import sys
import shutil
import subprocess
import os
from pathlib import Path
import readline

class Shell:
    def __init__(self):
        self.builtin = {
            "cd": self._cd,
            "echo": self._echo,
            "pwd": self._pwd,
            "type": self._type,
            "exit": self._exit,
        }
        self.BUILTIN = ["cd","pwd","type","exit","echo"]
        

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
    def get_dir_files(self,path='.') ->set[str]:
       """Return a set of filenames for all files (not directories) in the given path."""
       return {f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))}

    def completer(self, text, state):
        
        
          # Check if the character right before the cursor is a space
        line_buffer = readline.get_line_buffer()
        # print(f"text: {text}")
        # print(f"line_buffer: {line_buffer}")
        if "/" in line_buffer:
                    #split text into two path and prefix
                    parts = text.rsplit('/',1)
                    files = [f for f in os.listdir(parts[0]) 
                                if os.path.isfile(os.path.join(parts[0], f))]
                    options = sorted(c for c in files
                                        if c.startswith(parts[1]))
                    if state < len(options):
                        return parts[0]+ "/"+ options[state] + " "
                    return None
                    
        elif  ' ' in line_buffer:
            curr_dir_set = self.get_dir_files()
            # This executes only if Tab was pressed immediately after a space

            # Redisplay the prompt and current text to keep the UI clean
            # readline.forced_update_display()
            options = sorted(
                    c for c in curr_dir_set
                    if c.startswith(text)
                )
        
            if state < len(options):
                    return options[state] + " "
        
            return None
    
        else:
            exec_list = self.get_posix_executables()
            commands = set(self.BUILTIN)
            commands.update(exec_list)
                # Get the current cursor position
        
            # cursor_index = readline.get_begidx()
            
        
            options = sorted(
                c for c in commands
                if c.startswith(text)
            )

            if state < len(options):
                return options[state] + " "

            return None

    def run_program(
        self,
        command_list: list,
        stdout=None,
        stderr=None,
        stdout_append=False,
        stderr_append=False
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
           both builtin commands and executables """
        
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
            self.run_program(
                command_list,
                stdout,
                stderr,
                stdout_append,
                stderr_append
            )

    def _exit(
        self,
        args,
        stdout=sys.stdout,
        stderr=sys.stderr
    ) -> None:
        sys.exit(0)

    def _cd(
        self,
        args,
        stdout=sys.stdout,
        stderr=sys.stderr
    ) -> None:

        if not args:
            path = os.path.expanduser("~")
        else:
            path = os.path.expanduser(args[0])

        try:
            os.chdir(path)

        except OSError:
            stderr.write(
                f"cd: {path}: No such file or directory\n"
            )

    def _echo(
        self,
        args,
        stdout=sys.stdout,
        stderr=sys.stderr
    ):
        stdout.write(" ".join(args) + "\n")

    def _pwd(
        self,
        args,
        stdout=sys.stdout,
        stderr=sys.stderr
    ) -> None:
        stdout.write(os.getcwd() + "\n")

    def _type(
        self,
        args,
        stdout=sys.stdout,
        stderr=sys.stderr
    ) -> None:

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