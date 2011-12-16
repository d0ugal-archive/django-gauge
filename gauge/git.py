from subprocess import Popen, PIPE


def clone(repo, path):

    p = Popen(["git", "clone", repo, path], stdout=PIPE, stderr=PIPE)

    status_code = p.wait()

    if status_code != 0:
        raise Exception(p.stderr.read())

    return GitRepo(path)


class GitRepo(object):

    def __init__(self, path):
        self.path = path

    def call(self, command):

        p = Popen(command, cwd=self.path,
            stdout=PIPE, stderr=PIPE, close_fds=True)

        status_code = p.wait()

        if status_code != 0:
            raise Exception(p.stderr.read())

        return p.stdout, p.stderr

    def clean(self):
        return self.call(['git', 'clean', '-f'])

    def branches(self, remote=False):

        command = ['git', 'branch', ]
        if remote:
            command.appemd('-a')

        stdout, stderr = self.call(command)

        for line in stdout:
            line = line.strip()
            if line.startswith("* "):
                line = line[2:]

            yield line

    def create_tracking_branch(self, local, remote):

        return self.call(['git', 'branch', '--track', local, remote])
