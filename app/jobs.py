import subprocess


class Jobs:
    def __init__(self):
        self.jobs_list = []

    def run(self, command_list, stdout, stderr):
        process = subprocess.Popen(
            command_list,
            stdout=stdout,
            stderr=stderr
        )

        self.jobs_list.append(process)

        job_number = len(self.jobs_list)

        print(f"[{job_number}] {process.pid}")

    def list_jobs(self):
        for index, process in enumerate(self.jobs_list, start=1):
            print(f"[{index}] {process.pid}")