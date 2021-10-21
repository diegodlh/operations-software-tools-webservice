import os
import subprocess
import sys

from .ws import WebService


class PythonWebService(WebService):
    NAME = "uwsgi-python"
    QUEUE = "webgrid-generic"

    def check(self, wstype):
        src_path = self.tool.get_homedir_subpath("www/python/src")
        if not os.path.exists(src_path):
            raise WebService.InvalidWebServiceException(
                "Could not find ~/www/python/src. Are you sure you have a "
                "proper uwsgi application in ~/www/python/src?"
            )

    def run(self, port):
        super(PythonWebService, self).run(port)
        command = [
            "/usr/bin/uwsgi",
            # Will ignore plugins that don't load
            "--plugin",
            "python,python3",
            "--http-socket",
            ":" + str(port),
            "--chdir",
            self.tool.get_homedir_subpath("www/python/src"),
            "--logto",
            self.tool.get_homedir_subpath("uwsgi.log"),
            "--callable",
            "app",
            "--manage-script-name",
            "--workers",
            "4",
            "--mount",
            "/%s=%s"
            % (
                self.tool.name,
                self.tool.get_homedir_subpath("www/python/src/app.py"),
            ),
            "--die-on-term",
            "--strict",
            "--master",
        ]

        if os.path.exists(self.tool.get_homedir_subpath("www/python/venv")):
            command += [
                "--venv",
                self.tool.get_homedir_subpath("www/python/venv"),
            ]

        if os.path.exists(
            self.tool.get_homedir_subpath("www/python/uwsgi.ini")
        ):
            command += [
                "--ini",
                self.tool.get_homedir_subpath("www/python/uwsgi.ini"),
            ]

        subprocess.check_call(
            command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
        )
