import sys

## bug where entering nothing 
class shell:
    def __init__(self,_input):
        self._input = _input

    def builtin_exit(self):
        if self.command == "exit":
            sys.exit(0)

    def test_print_command(self):
        print(self.command)



def main():
    init_input = input()

    sh = shell(init_input)
    
    while(1):
        sys.stdout.write("$ ")
        command = input()
        sh.builtin_exit()
        sh.test_print_command()
        sys.stdout.flush()



if __name__ == "__main__":
    main()