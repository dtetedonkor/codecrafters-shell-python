import shutil
import subprocess
import sys
import os

BUILTINS = {"exit", "echo", "type","pwd","cd"}
def quote_parser(user_input: str) -> list:
    
    in_quotes = False
    in_double_quotes = False
    temp = list()
    res = list()
    for _ in user_input:

        if _ == '"':
            in_double_quotes = not in_double_quotes

        # condition for when double quotes with a single quote in it 

        if _ == "'" and in_double_quotes:
            temp.append(_)
            continue

        if _ == "'" or _ == '"':
            in_quotes = not in_quotes
        elif _ == " " and in_quotes == False:
            if temp:
                res.append("".join(temp))
            temp.clear()
        else:
            temp.append(_)
    res.append("".join(temp)) 
    temp.clear() 
    return res

def backslash_parser(user_input: str) -> list:
  
    res = list()
    temp = list()
    backslash = False 
    for _ in user_input:
        if _ == "\\" and not backslash:
            backslash = True
            continue

        if _ == " " and backslash:
            temp.append(_)
            backslash = False
        elif _ == " " and not backslash:
            if temp:
                res.append("".join(temp))
            temp.clear()
        else:
            temp.append(_)
            backslash = False
    res.append("".join(temp)) 
    temp.clear() 
    return res
    
def parser_input(user_input: str) -> list:
    """at some point will change to only perform certain parsing if """
    char_set = set(user_input)
    

    if "\\" in char_set:
        parsed_input  = backslash_parser(user_input)
        return parsed_input
    
    if "'" in char_set or '"' in char_set:
        parsed_input = quote_parser(user_input)
        return parsed_input
    else:
        parsed_input = user_input.split()
        return parsed_input
    
def pwd_builtin() -> None: 
    print(os.getcwd())

def my_shell() -> list:
    
    sys.stdout.write("$ ")
    _input  = input()
    return parser_input(_input)
    

def builtin_check(command_list :list)  -> list:
    return command_list and command_list[0] in BUILTINS


def exit_builtin()-> None:
    """Return True if the shell should exit."""
    sys.exit(0)


def echo_builtin(_args: str) -> None:
    """Implement the echo builtin."""

    print(_args)


def type_builtin(command_list: list) -> None:
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


def run_builtin(command_list: list) -> None:
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