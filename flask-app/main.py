from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['GET'])
def verify():
    # Respond to the webhook verification (GET request)
    # by echoing back the challenge parameter
    return request.args.get('challenge')

@app.route("/hello")
def hello_world():
    return "Hello World from Flask"

@app.route("/")
def main():
    index_path = os.path.join(app.static_folder, 'index.html')
    return send_file(index_path)

# For Angular SPA routes
@app.route('/<path:path>')
def route_frontend(path):
    # Serve static files
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # Or angular routes
    else:
        index_path = os.path.join(app.static_folder, 'index.html')
        return send_file(index_path)

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)