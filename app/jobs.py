import subprocess


class Job:
    def __init__(self, job_number, process, command):
        self.job_number = job_number
        self.process = process
        self.command = command
        self.marker = " "
        self.done_reported = False

    def is_done(self):
        return self.process.poll() is not None

    def status(self):
        return "Done" if self.is_done() else "Running"


class Jobs:
    def __init__(self):
        self.jobs_list = []
        self.next_job_number = 1

    def run(self, command_list, stdout, stderr):
        process = subprocess.Popen(
            command_list,
            stdout=stdout,
            stderr=stderr
        )

        job = Job(
            job_number=self.next_job_number,
            process=process,
            command=command_list
        )

        self.jobs_list.append(job)

        self.update_markers()

        print(f"[{job.job_number}] {process.pid}")

        self.next_job_number += 1

    def update_markers(self):
        # First clear every marker
        for job in self.jobs_list:
            job.marker = " "

        # Last job is +
        if len(self.jobs_list) >= 1:
            self.jobs_list[-1].marker = "+"

        # Second-to-last job is -
        if len(self.jobs_list) >= 2:
            self.jobs_list[-2].marker = "-"

    def reap_reported_jobs(self):
        for i in range(len(self.jobs_list) - 1, -1, -1):

            job = self.jobs_list[i]

            if job.is_done() and job.done_reported:
                self.jobs_list.pop(i)

        self.update_markers()

    def list_jobs(self, stdout):
        self.reap_reported_jobs()

        for job in self.jobs_list:

            print(
                f"[{job.job_number}]{job.marker}  "
                f"{job.status():<24}",
                *job.command,
                file=stdout
            )

            if job.is_done():
                job.done_reported = True