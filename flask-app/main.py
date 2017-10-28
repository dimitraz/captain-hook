from flask import Flask, Response, request, jsonify, render_template
from hashlib import sha256
from redis import StrictRedis
import os
import time
import hmac
import boto3
import config
import logging
import dropbox
import threading

app = Flask(__name__)

# Initialise Redis, dropbox, s3 clients
redis = StrictRedis('redis-py', 6379, charset='utf-8', decode_responses=True)
dbx = dropbox.Dropbox(config.DBX_ACCESS_TOKEN)
s3 = boto3.resource(
    's3', 
    aws_access_key_id=config.AWS_ACCESS_KEY,
    aws_secret_access_key=config.AWS_SECRET_KEY
)

@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.DEBUG)
    redis.set('wait', 'false')

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

    app.logger.info('Responding to webhook...')

    # Cursor to only get latest changes
    cursor = redis.get('cursor')
    has_more = True

    # Store entry name and path in redis keystore
    while has_more:
        if cursor is None:
            result = dbx.files_list_folder('')
        else:
            result = dbx.files_list_folder_continue(cursor)

        for entry in result.entries:
            # Ignore deleted files, folders, and non-image based files
            if (isinstance(entry, dropbox.files.DeletedMetadata) or isinstance(entry, dropbox.files.FolderMetadata) or
            not entry.path_lower.endswith(('.jpeg', '.jpg', '.png', '.gif'))): 
                continue
            
            app.logger.info('Saving entry: %s to redis', entry.name)
            redis.set(entry.name, entry.path_lower)
                
        # Update cursor
        cursor = result.cursor
        redis.set('cursor', cursor)

        # Repeat only if there's more to do
        has_more = result.has_more

    threading.Thread(target=process_files).start()
    res = Response(status=200, mimetype='application/json')
    return res

# Get newest files and upload to s3
def process_files():
    app.logger.info('Beginning to process files')

    # Download file and upload to s3 bucket
    for key in redis.scan_iter(): 
        if key not in ['cursor', 'wait'] and redis.get(key) != 'processed':
            app.logger.info('Attempting to upload file: %s to s3 bucket', key)
            md, res = dbx.files_download(redis.get(key))
            data = res.content
            response = s3.Object(config.S3_BUCKET_NAME, key).put(ACL='public-read', Body=data)
            app.logger.info(response)
            redis.set(key, 'processed')
    
    app.logger.info('Finished uploading files')
    res = Response(status=200, mimetype='application/json')
    return res

@app.route("/")
def main():
    urls = []
    bucket = s3.Bucket(config.S3_BUCKET_NAME)
    region = config.AWS_REGION_NAME

    for item in bucket.objects.all():
        url = 'https://s3-' + region + '.amazonaws.com/' + config.S3_BUCKET_NAME + '/' + item.key
        urls.append(url)

    return render_template('index.html', urls=urls)

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)