import sys
from pathlib import Path


        

def main():
    # TODO: Uncomment the code below to pass the first stage
    sh_builtin = {"exit","type","echo"} #builtin set for quick retreval 
    while(1):
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break

        command_list = command.split()
        arguments = ' '.join(command_list[1:])

        if command_list[0] == "echo": #echo builtin
            print(arguments)
            continue

        if command_list[0] == "type": # type builtin handeling
            if arguments in sh_builtin:
                print(f"{arguments} is a shell builtin")
            else:
                print(f"{arguments}: not found")
            continue

        print(f"{command.rstrip()}: command not found")
        
        

    

    pass

    




if __name__ == "__main__":
    main()
