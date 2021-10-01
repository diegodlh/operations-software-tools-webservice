import os
import subprocess
import sys

from .ws import WebService


class UwsgiWebService(WebService):
    NAME = "uwsgi-plain"
    QUEUE = "webgrid-generic"

    def check(self, wstype):
        src_path = self.tool.get_homedir_subpath("uwsgi.ini")
        if not os.path.exists(src_path):
            raise WebService.InvalidWebServiceException(
                "Could not find ~/uwsgi.ini. Are you sure you have a "
                "proper uwsgi config setup in ~/uwsgi.ini?"
            )

    def run(self, port):
        super(UwsgiWebService, self).run(port)
        command = [
            "/usr/bin/uwsgi",
            "--http-socket",
            ":" + str(port),
            "--logto",
            self.tool.get_homedir_subpath("uwsgi.log"),
            "--ini",
            self.tool.get_homedir_subpath("uwsgi.ini"),
            "--workers",
            "4",
            "--die-on-term",
            "--strict",
            "--master",
        ]

        subprocess.check_call(
            command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
        )
