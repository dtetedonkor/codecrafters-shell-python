import subprocess
import sys
import shutil
class Pipe:
    def __init__(self):
        self.pipeio = None
        
        # command : output
        """ we want
            output --> input  """

    def execute(
           self,
           pipe_list: list[list],
           stdout = None,
           stderr = None,
           stdout_append = False,
           stderr_append = False,):
           for cmd in pipe_list:
                self.run(cmd,stdout,stderr)
           sys.stdout.write(self.pipeio)
           
           
    def run(self,cmd,stdout_dest,stderr_dest):
        
        program = shutil.which(cmd[0])
        
        # Program doesn't exist
        if not program:
            print(f"{cmd[0]}: command not found")
            return

        result = subprocess.run(
                    cmd,
                    input= self.pipeio,
                    text=True,
                    capture_output=True,
                    check=True
                )
        
        self.pipeio = result.stdout
       