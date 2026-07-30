import shutil
import subprocess
import sys
import os

BUILTINS = {"exit", "echo", "type","pwd","cd"}

def pwd_builtin() -> None:
    """Implement echo builtin."""
    print(os.getcwd())

def my_shell():
    """Read a command from the user."""
    sys.stdout.write("$ ")
    return input().split()


def builtin_check(command_list :list)  -> list:
    """Return True if the command is a shell builtin."""
    return command_list and command_list[0] in BUILTINS


def exit_builtin(command_list: list):
    """Return True if the shell should exit."""
    return command_list[0] == "exit"


def echo_builtin(command_list: list) -> None:
    """Implement the echo builtin."""
    arguments = " ".join(command_list[1:])
    print(arguments)


def type_builtin(command_list: list):
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

## change this to a switch statent in the future for now keep
def run_builtin(command_list: list):
    """Dispatch to the appropriate builtin."""
    command: str = command_list[0]
    arguments = " ".join(command_list[1:])

    match command:
        case "echo":
            echo_builtin(command_list)

        case "type":
            type_builtin(command_list)

        case "pwd":
            pwd_builtin()

        case "cd":
            cd_builtin(arguments)


def run_program(command_list: list) -> None:
    """Run an external program."""
    program  = shutil.which(command_list[0])

    if program:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
        )
        sys.stdout.write(result.stdout)
    else:
        print(f"{command_list[0]}: command not found")

def cd_builtin(_args: list) -> None:
    try:
        os.chdir(_args)
    except:
        print(f"cd: {_args}: No such file or directory")

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