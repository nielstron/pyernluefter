import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
try:
    from http import HTTPStatus
except ImportError:
    # Backwards compatability
    import http.client as HTTPStatus
from pathlib import Path

SERVER_DIR = Path(__file__).parent or Path('.')


class BayernLuftServer(HTTPServer):

    blocked = False

    def set_blocked(self):
        self.blocked = True

    def unset_blocked(self):
        self.blocked = False


class BayernLuftHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.server.blocked:
            self.send_error(403, "Access denied because server blocked")
        else:
            super(BayernLuftHandler, self).do_GET()

    def translate_path(self, path:str):
        """
        translate paths for the two files we provide
        """
        path = path.lstrip('/')
        server_path = str(SERVER_DIR.absolute())
        if path.endswith("?export=1") and (path.startswith("?") or path.startswith("index.html")):
            return os.path.join(server_path, "?export=1")
        elif path == "export.txt":
            return os.path.join(server_path, "export.txt")
        return os.path.join(server_path, "nothingtobefound")

    def send_error(self, code, message=None, explain=None):
        """
        Send syncthru error page
        :param code:
        :param message:
        :param explain:
        :return:
        """
        self.log_error("code %d, message %s", code, message)
        self.send_response(code, message)
        self.send_header('Connection', 'close')

        # Message body is omitted for cases described in:
        #  - RFC7230: 3.3. 1xx, 204(No Content), 304(Not Modified)
        #  - RFC7231: 6.3.6. 205(Reset Content)
        body = None
        if (code >= 200 and
                code not in (HTTPStatus.NO_CONTENT, HTTPStatus.RESET_CONTENT,
                             HTTPStatus.NOT_MODIFIED)):
            # HTML encode to prevent Cross Site Scripting attacks
            # (see bug #1100201)
            # Specialized error method for fronius
            with SERVER_DIR.joinpath(".error.html").open('rb') as file:
                body = file.read()
            self.send_header("Content-Type", self.error_content_type)
            self.send_header('Content-Length', int(len(body)))
        self.end_headers()

        if self.command != 'HEAD' and body:
            self.wfile.write(body)
