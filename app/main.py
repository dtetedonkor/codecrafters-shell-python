import sys
import shutil
import subprocess

def type_builtin(command_list) -> None:
    sh_builtin = {"exit","type","echo"} #builtin set for quick retreval
    arguments = ' '.join(command_list[1:])
    if command_list[0] == "type": # type builtin handeling
                if arguments in sh_builtin:
                    print(f"{arguments} is a shell builtin")
                elif shutil.which(arguments):
                    print(shutil.which(arguments))
                else:
                    print(f"{arguments}: not found")

def exit_bultin(command_list) -> bool:
           if ' '.join(command_list) == "exit":
                return True 
           return False 

def echo_builtin(command_list) -> None:
       
       arguments = ' '.join(command_list[1:])
       if command_list[0] == "echo": #echo builtin
                  print(arguments)
def builtin_check (command_list) -> bool:
       sh_builtin = {"exit","type","echo"}
       if command_list[0] in sh_builtin:
              return True
       return False

def  run_program(command_list) -> None:
         if shutil.which(command_list[0]):
                   pl = subprocess.run(command_list,
                                     capture_output=True,
                                     text=True) 
                   sys.stdout.write(pl.stdout) 
         else:
             print(f"{' '.join(command_list)}: command not found")   
     
def my_shell() -> list:
    
  
        sys.stdout.write("$ ")
        command = input()

        command_list = command.split()

        return command_list
                       
        

def main():
    while(1):
        sh = my_shell()
        if exit_bultin(sh):
              break
        if builtin_check:
            echo_builtin(sh)
            type_builtin(sh)
        else:
              run_program(sh)
        
               

        
        
        

    


    




if __name__ == "__main__":
    main()
