from shell import Shell
from parser import _Parser

def main():
    parser = _Parser()
    shell = Shell()

    while True:
        user_in = input("$ ")

        if not user_in:
            continue

        parsed_input = parser.parse(user_in)

        if not parsed_input:
            continue

        shell.execute(parsed_input)


if __name__ == "__main__":
    main()