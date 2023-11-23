from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class PreProcessingHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        message = ""
        content_length = int(self.headers['Content-Length'])
        post_content = {"post_data": self.rfile.read(content_length), "post_json": {}}

        if not self.handled_request_body(post_content):
            return

        if self.path == '/tripleconstruction':
            try:
                for f in post_content['post_json']:
                    for sentence in f["sentences"]:
                        for em in sentence["entityMentions"]:
                            print(em["name"])
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                message = "Post request was successfully processed. Relation extraction and concept linking has begun " + post_content['post_data']
            except:
                self.wrongly_formatted_request_response()
                return
        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
            message = "Invalid endpoint"

        self.wfile.write(bytes(message, "utf8"))

    def wrongly_formatted_request_response(self):
        self.send_response(422)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes("The request body was incorrectly formatted", "utf8"))

    def handled_request_body(self, post_content):
        try:
            post_content['post_data'] = post_content['post_data'].decode('utf-8')
            post_content['post_json'] = json.loads(post_content['post_data'])
            return True
        except:
            self.wrongly_formatted_request_response()
            return False


if __name__ == '__main__':
    with HTTPServer(('', 8000), PreProcessingHandler) as server:
        print("Hosting server on 0.0.0.0:8000")
        server.serve_forever()
