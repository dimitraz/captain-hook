# captain-hook
A photo app with flask, ec2, s3 and dropbox webhooks inspired by [`PhotosOfBlacklion/captain-hook`](https://github.com/PhotosOfBlacklion/captain-hook).

## Register a Dropbox app
* Register a Dropbox app with `App Folder` access [here](https://www.dropbox.com/developers/apps) 
* Generate a new Dropbox OAuth 2 token 
* Update `config.py` with your App secret, OAuth token and AWS credentials (make sure you've granted full s3 and ec2 access):
```python
DBX_SECRET = b'xxxxxxxxxxxxxxx'
DBX_ACCESS_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
AWS_ACCESS_KEY = 'xxxxxxxxxxxxxxxxxx'
AWS_SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

## Start the application 
Start the application by running:
```bash
python3 main.py --key <your-pem-key>
```
This will do the following:
* Create a new ec2 instance (or use an existing one, if you provide an existing `instance ID` with the `--ec2` flag)
* Create a new s3 bucket (or use an existing one, if you provide an existing `bucket name` with the `--s3` flag)
* Run a container with a flask application to process incoming webhooks

### Options
```bash
python3 main.py --key <your-pem-key> [options]

Options:
  --ec2   Name of ec2 instance (if it exists, that instance will be used)   
                                                            [Default: captain-hook]
  --s3    Name of s3 bucket (if it exists, that bucket will be used)        
                                                            [Default: {0:%Y-%m-%d-%H.%M.%S-hook}]

Examples: 
  python3 main.py --key aws-key.pem --ec2 cool-instance --s3 cool-bucket-name
  python3 main.py --key aws-key.pem --ec2 i-05b7ea9dca0117fb9 --s3 2017-10-28-10.55.31-hook
```

## Test it out
* In your Dropbox application settings, register the webhook endpoint. This should look like: `http://<ec2-instance-public-ip>/webook`
* Upload a few images to the newly created Dropbox App folder. 
* Wait for the application to do its magic! Your images should be displayed at your instance's ip address.

To view the logs, connect to your instance and run `docker logs <container-id>`