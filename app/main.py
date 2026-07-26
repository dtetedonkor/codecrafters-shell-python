import sys
import shutil
import subprocess


        

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
            elif shutil.which(arguments):
                print(shutil.which(arguments))
            else:
                print(f"{arguments}: not found")
            continue

        if shutil.which(command_list[0]):
            subprocess.run(command_list,
                              capture_output=True,
                              text=True,
                              check=True)    

        print(f"{command.rstrip()}: command not found")
        
        

    


    




if __name__ == "__main__":
    main()
