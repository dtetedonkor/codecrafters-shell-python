import os
from contextlib import ExitStack


class History:
    def __init__(self):
        self.history_list = []
        self.written_count = 0


    def hist_init(self, envir= None):
        if envir:
            self.read(envir)

    def read(self, path):
        if os.path.exists(path):
            with ExitStack() as stack:
                file = stack.enter_context(open(path, "r"))
                for line in file:
                    self.history_list.append(line.strip())

    def write(self, path):
        with ExitStack() as stack:
            file = stack.enter_context(open(path, "w"))
            for cmd in self.history_list:
                file.write(cmd + "\n")

    def append(self, path):
        new_items = self.history_list[self.written_count:]

        if not new_items:
            return

        with open(path, "a") as f:
            for line in new_items:
                f.write(line if line.endswith("\n") else line + "\n")

        self.written_count = len(self.history_list)

    def display(self, recent=None):
        last_index = len(self.history_list) - 1

        if recent is None:
            recent = last_index + 1

        for index, cmd in enumerate(self.history_list):
            if index > last_index - recent:
                print(f"{index + 1} {cmd}")