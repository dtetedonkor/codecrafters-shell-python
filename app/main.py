import readline
from .parser import Parser
from .shell import Shell
from .completer import Completer
from .jobs import Jobs
from .pipe import Pipe
import asyncio

def main():
    parser = Parser()
    completer = Completer()
    jobs = Jobs()
    pipe = Pipe()
    shell = Shell(completer,jobs,pipe)
    
    # Fetch current word delimiters
    current_delims = readline.get_completer_delims()

    # Remove the hyphen from the delimiter string
    new_delims = current_delims.replace("-", "")
    readline.set_completer_delims(new_delims)
    readline.set_completer(completer.completer)
    readline.parse_and_bind("Tab: Complete")
    
    while True:
        
        user_in = input("$ ")
        if not user_in:
            continue

        try:
            parsed_input = parser.parse(user_in)
        except ValueError as e:
            print(f"shell: {e}")
            continue

        if not parsed_input:
            continue

        shell.execute(parsed_input)
        jobs.check_done()
        


if __name__ == "__main__":
    main()
