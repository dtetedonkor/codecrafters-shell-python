import os
from .parser import Parser
from .shell import Shell
from .completer import Completer
from .jobs import Jobs
from .pipe import Pipe
from .history import History


def main():
    parser = Parser()
    completer = Completer()
    jobs = Jobs()
    pipe = Pipe()
    history  = History()
    shell = Shell(completer,jobs,pipe,history)
    HIST_FILE = os.environ.get("HISTFILE")
    completer.comp_init()
    history.hist_init(HIST_FILE)
    
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
