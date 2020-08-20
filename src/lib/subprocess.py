"""Standard library"""
import subprocess


class Command:
    """An external command class to emulate and call external processes on the
    host machine."""

    def __init__(self, command_name):
        self.command_name = command_name

    def run(self, *args):
        arguments = " ".join(args)
        command = "{0} {1}".format(self.command_name, arguments)
        return subprocess.Popen(
            command,
            shell=True,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            executable="/bin/bash",
        )

    def prefix_run(self, prefix, *args):
        arguments = " ".join(args)
        command = "{0} {1} {2}".format(prefix, self.command_name, arguments)
        return subprocess.Popen(
            command,
            shell=True,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            executable="/bin/bash",
        )
