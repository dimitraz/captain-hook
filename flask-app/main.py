from flask import Flask, request, jsonify
from hashlib import sha256
import os
import hmac
import config
import logging

app = Flask(__name__)

@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.DEBUG)

# Webhook verification request
@app.route('/webhook', methods=['GET'])
def verify():
    return request.args.get('challenge')

# Respond to webhooks
@app.route('/webhook', methods=['POST'])
def webhook():
    # Make sure this is a valid request from Dropbox
    signature = request.headers.get('X-Dropbox-Signature')
    if not hmac.compare_digest(signature, hmac.new(config.DBX_SECRET, request.data, sha256).hexdigest()):
        abort(403)

    return 'ok'

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