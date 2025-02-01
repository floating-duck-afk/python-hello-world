from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse
import os

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # Enable CORS (allow requests from any origin)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            # Parse query parameters (e.g., ?name=X&name=Y)
            query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            names = query_components.get('name', [])

            # Check if names were provided in the query
            if not names:
                self.send_response(400)
                self.wfile.write(b"Error: 'name' query parameter is required")
                return

            # Load the data from data.json
            data_file = 'data.json'

            # Ensure the file exists
            if not os.path.exists(data_file):
                self.send_response(500)
                self.wfile.write(b"Error: data.json file not found")
                return

            with open(data_file, 'r') as f:
                data = json.load(f)

            # Prepare the marks for the requested names
            marks = []
            for name in names:
                # Check if name exists in the JSON data
                if name in data:
                    marks.append(data[name]['marks'])
                else:
                    marks.append(None)

            # Create the response JSON object
            response = json.dumps({"marks": marks})

            # Send the response
            self.wfile.write(response.encode('utf-8'))

        except FileNotFoundError:
            # If the file doesn't exist, send an error
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Error: data.json file not found")

        except Exception as e:
            # Handle any other unexpected errors
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Internal server error")
            print(f"Error: {e}")


# Set up and run the server
def run(server_class=HTTPServer, handler_class=Handler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
