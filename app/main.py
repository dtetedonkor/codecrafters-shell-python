import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while(1):
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break

        command_list = command.split()

        if command_list[0] == "echo":
            print(' '.join(command_list[1:]))
            continue



        print(f"{command.rstrip()}: command not found")
        
        

    

    pass

    




if __name__ == "__main__":
    main()
