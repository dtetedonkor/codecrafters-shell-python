import shutil
import subprocess
import sys
import os
BUILTINS = {"exit", "echo", "type","pwd"}

def pwd_builtin() -> None:
        print(os.getcwd())

def my_shell():
    """Read a command from the user."""
    sys.stdout.write("$ ")
    return input().split()


def builtin_check(command_list):
    """Return True if the command is a shell builtin."""
    return command_list and command_list[0] in BUILTINS


def exit_builtin(command_list):
    """Return True if the shell should exit."""
    return command_list[0] == "exit"


def echo_builtin(command_list):
    """Implement the echo builtin."""
    arguments = " ".join(command_list[1:])
    print(arguments)


def type_builtin(command_list):
    """Implement the type builtin."""
    command = command_list[1]

    if command in BUILTINS:
        print(f"{command} is a shell builtin")
    else:
        program = shutil.which(command)
        if program:
            print(program)
        else:
            print(f"{command}: not found")


def run_builtin(command_list):
    """Dispatch to the appropriate builtin."""
    command = command_list[0]

    if command == "echo":
        echo_builtin(command_list)

    elif command == "type":
        type_builtin(command_list)
    elif command == "pwd":
        pwd_builtin(command_list)


def run_program(command_list):
    """Run an external program."""
    program = shutil.which(command_list[0])

    if program:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
        )
        sys.stdout.write(result.stdout)
    else:
        print(f"{command_list[0]}: command not found")


def main():
    while True:
        command_list = my_shell()

        # Ignore blank lines
        if not command_list:
            continue

        # Exit builtin
        if exit_builtin(command_list):
            break

        # Builtins
        if builtin_check(command_list):
            run_builtin(command_list)
        else:
            run_program(command_list)


if __name__ == "__main__":
    main()