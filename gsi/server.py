from http.server import BaseHTTPRequestHandler, HTTPServer
from operator import attrgetter
from threading import Thread
import json

from . import gamestate
from . import payloadparser


class GSIServer(HTTPServer):
    def __init__(self, server_address, auth_token, callback):
        super(GSIServer, self).__init__(server_address, RequestHandler)

        self.auth_token = auth_token
        self.gamestate = gamestate.GameState()
        self.gamestate_raw = None
        self.parser = payloadparser.PayloadParser()
        self.callback = callback

        self.running = False

    def start_server(self):
        try:
            thread = Thread(target=self.serve_forever, daemon=True)
            thread.start()
            print("Server started")
        except:
            print("Could not start server.")

    def get_info(self, target, *argv):
        try:
            if len(argv) == 0:
                state = attrgetter(f"{target}")(self.gamestate)
            elif len(argv) == 1:
                state = attrgetter(f"{target}.{argv[0]}")(self.gamestate)
            elif len(argv) == 2:
                state = attrgetter(f"{target}.{argv[0]}")(self.gamestate)[f"{argv[1]}"]
            else:
                print("Too many arguments.")
                return False
            if "object" in str(state):
                return vars(state)
            else:
                return state
        except Exception as E:
            print(E)
            return False


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")

        payload = json.loads(body)

        if not self.authenticate_payload(payload):
            print("auth_token does not match.")
            return False
        else:
            self.server.running = True

        self.server.parser.parse_payload(payload, self.server.gamestate)
        self.server.gamestate_raw = payload
        self.server.callback(self.server.gamestate)

    def do_GET(self):
        if not self.server.gamestate_raw:
            self.send_response(401)
            self.end_headers()

        print(self.server.gamestate_raw)
        data = json.dumps(self.server.gamestate_raw)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data.encode(encoding="utf_8"))

    def authenticate_payload(self, payload):
        if "auth" in payload and "token" in payload["auth"]:
            return payload["auth"]["token"] == self.server.auth_token
        else:
            return False
