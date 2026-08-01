class Shell:
    def __init__(self):
        self.running = True

    def run_command(self, command):
        print(f"Running: {command}")


def main():
    shell = Shell()

    while shell.running:
        command = input("$ ")
        shell.run_command(command)


if __name__ == "__main__":
    main()