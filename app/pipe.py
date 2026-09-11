import subprocess
import sys
import shutil


class Pipe:
    def __init__(self):
        self.pipeout = None
        self.piperr = None

    def execute(
        self,
        pipe_list: list[list],
        stdout=None,
        stderr=None,
        stdout_append=False,
        stderr_append=False,
    ):
        stdout = subprocess.PIPE
        processes = []

        for index, cmd in enumerate(pipe_list):
            if index == len(pipe_list) - 1:
                stdout = None

            proc = self.run(cmd, stdout, stderr)
            processes.append(proc)

        # Wait for the final command
        processes[-1].wait()

    def run(self, cmd, stdout_dest, stderr_dest):

        program = shutil.which(cmd[0])

        if not program:
            print(f"{cmd[0]}: command not found")
            return

        proc = subprocess.Popen(
            cmd,
            stdin=self.pipeout,
            stdout=stdout_dest,
            stderr=stderr_dest,
            text=True,
        )

        # The parent no longer needs its copy of the previous pipe
        if self.pipeout:
            self.pipeout.close()

        self.pipeout = proc.stdout

        return proc