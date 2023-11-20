from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class PreProcessingHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        post_json = json.loads(post_data)

        if self.path == '/tripleconstruction':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            for f in post_json:
                for sentence in f["sentences"]:
                    for em in sentence["entityMentions"]:
                        print(em["name"])
            message = "POST to group-c data: " + post_data
            
        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()

            message = "Invalid endpoint"

        self.wfile.write(bytes(message, "utf8"))

if __name__ == '__main__':
    with HTTPServer(('', 8000), PreProcessingHandler) as server:
        print("Hosting server on 0.0.0.0:8000")
        server.serve_forever()
