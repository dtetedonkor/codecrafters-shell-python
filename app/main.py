from .shell import Shell
from .parser import _Parser
import readline

def main():
    parser = _Parser()
    shell = Shell()
    readline.set_completer(shell.completer)
    readline.parse_and_bind("tab: Complete")
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


if __name__ == "__main__":
    main()