from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse query parameters
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        # Get 'name' parameters from the query string
        names = query_components.get('name', [])
        
        # Load the JSON data (assuming the JSON structure you have)
        with open('data.json', 'r') as f:
            data = json.load(f)
        
        # Prepare the list of marks for the given names
        marks = []

        # Loop through the names and retrieve the marks from the data
        for name in names:
            if name in data:
                marks.append(data[name]['marks'])
            else:
                marks.append(None)  # If name is not found, append None
        
        # Create the response in the required format
        response = json.dumps({"marks": marks})

        # Send the response back to the client
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
        return

# Set up the server
def run(server_class=HTTPServer, handler_class=handler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
