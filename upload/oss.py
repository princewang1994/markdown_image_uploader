import json
import oss2
import os

def read_config():
    config_dir = os.path.join(os.environ['HOME'], '.oss')
    config_path = os.path.join(config_dir, 'oss.conf')

    # if config file not exist, make blank one
    if not os.path.exists(config_path):
        print('Config file not found, making blank config file to `{}`'.format(config_path))
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)
        make_blank_config(config_path)

    config = json.load(open(config_path))
    return config

def make_blank_config(config_file):
    config = {
        'endpoint': 'Your Endpoint(Without http://)',
        'ak': 'Your AccessKey',
        'sk': 'Your SecretKey',
        'bucket': 'Your Bucket Name'
    }
    text = json.dumps(config, indent=4)
    with open(config_file, 'w') as f:
        f.write(text)

def upload_to_oss(filename, path, config):
    """
    Params: 
        filename(str): filename in oss
        path(str): local file path
        config: oss config
    Returns:
        object url
    """
    # authentication
    ak = config['ak']
    sk = config['sk']
    endpoint = config['endpoint']
    bucket_name = config['bucket']
    auth = oss2.Auth(ak, sk)
    bucket = oss2.Bucket(auth, 'http://' + endpoint, bucket_name)

    try:
        result = bucket.put_object_from_file(filename, path)
        if result.status != 200:
            raise Exception
        # generate url
        url = 'http://{}.{}/{}'.format(bucket_name, endpoint, filename)
        return url
    except:
        print('Upload {} failed.'.format(path))
        raise
