import shutil
import subprocess
import sys
import os

BUILTINS = {"exit", "echo", "type","pwd","cd"}

def parser_input(user_input: str) -> list:

    in_quotes = False
    temp = list()
    res = list()
    for _ in user_input:
        if _ == "'":
            # res.append("".join(temp))
            # temp.clear()
            in_quotes = not in_quotes
            continue
        
        if _ == " " and in_quotes == True:
            temp.append(_)
        if _ == " " and in_quotes == False:
            if temp:
                res.append("".join(temp))
            temp.clear()
            continue
        temp.append(_)
    res.append("".join(temp)) 
    temp.clear() 
    return res

def pwd_builtin() -> None:
    """Implement echo builtin."""
    print(os.getcwd())

def my_shell() -> list:
    """Read a command from the user."""
    
    sys.stdout.write("$ ")
    _input  = input()
    parsed_input  = parser_input(_input)
    return parsed_input

def builtin_check(command_list :list)  -> list:
    """Return True if the command is a shell builtin."""
    return command_list and command_list[0] in BUILTINS


def exit_builtin()-> None:
    """Return True if the shell should exit."""
    sys.exit(0)


def echo_builtin(_args: str) -> None:
    """Implement the echo builtin."""

    print(_args)


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
        case "exit":
            exit_builtin()
        case "echo":
            echo_builtin(arguments)
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

def cd_builtin(_args: str) -> None:
  
        if _args ==  '~':
            try:
                os.chdir(os.getenv("HOME"))
            except OSError:
                print(f"cd: {_args}: No such file or directory")
            
        else:
             try:
                os.chdir(_args)
             except OSError:
                print(f"cd: {_args}: No such file or directory")
                        
    

def main():

    
    while True:
        command_list = my_shell()

        # Ignore blank lines
        if not command_list:
            continue

        # Builtins
        if builtin_check(command_list):
            run_builtin(command_list)
        else:
            run_program(command_list)


if __name__ == "__main__":
    main()