import readline

from .parser import Parser
from .shell import Shell


def main():
    parser = Parser()
    shell = Shell()
    # Fetch current word delimiters
    current_delims = readline.get_completer_delims()

    # Remove the hyphen from the delimiter string
    new_delims = current_delims.replace("-", "")
    readline.set_completer_delims(new_delims)
    readline.set_completer(shell.completer)
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


if __name__ == "__main__":
    main()
