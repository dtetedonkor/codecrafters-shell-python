import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    sys.stdout.write("$ ")
    command = sys.stdin.readline()
    print(f"{command.rstrip()}: command not found")

    pass

    




if __name__ == "__main__":
    main()
