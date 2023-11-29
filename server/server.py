from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from relation_extraction.NaiveMVP.main import handle_relation_post_request

class PreProcessingHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print("recieved post request...")
        message = ""
        content_length = int(self.headers['Content-Length'])
        post_content = {"post_data": self.rfile.read(content_length), "post_json": {}}

        if self.headers.get("Access-Authorization").__str__() != os.getenv("API_SECRET"):
            message = "Unauthorized"
            self.send_response(401)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(f"Error occured! {message}", "utf8"))
            return

        if not self.handled_request_body(post_content):
            return

        if self.path == '/tripleconstruction':
            try:
                handle_relation_post_request(post_content["post_json"])
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                message = "Post request was successfully processed. Relation extraction and concept linking completed\n"
            except Exception as E:
                self.wrongly_formatted_request_response(str(E))
                return
        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
            message = "Invalid endpoint"

        self.wfile.write(bytes(message, "utf8"))

    def wrongly_formatted_request_response(self, message):
        self.send_response(422)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(f"Error occured! {message}", "utf8"))

    def handled_request_body(self, post_content):
        try:
            post_content['post_data'] = post_content['post_data'].decode('utf-8')
            post_content['post_json'] = json.loads(post_content['post_data'])
            return True
        except:
            self.wrongly_formatted_request_response("Error occured!")
            return False


if __name__ == '__main__':
    with HTTPServer(('', 80), PreProcessingHandler) as server:
        print("Hosting server on 0.0.0.0:80")
        server.serve_forever()
