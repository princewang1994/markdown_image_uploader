import os
import time
import argparse
import random
import copy
import subprocess
import configparser
from PIL import Image

# global variables
ak, sk, url, bucket, args = None, None, None, None, None
debug = None

def make_blank_config(config_file):
    """Generate blank config
    Parameters:
        ak: app key
        sk: secret key
        url: prefix
        bucket: bucket in QiNiu
    Example:
        [qiniu]
        ak=F9-lVHzO3KWKAAbJA_FYTL1l8WEx2fJuNubSJXRv
        sk=wEg_xzmOCaYqzZQEEE87sfkJ2-wfYCYfgKy7Bi7Y
        url=http://oodd7tmt5.bkt.clouddn.com/
        bucket=mypicbed
    """

    config = configparser.RawConfigParser(allow_no_value=True)
    config.add_section('qiniu')

    config.set('qiniu', 'ak', value='your QiNiu AppKey')
    config.set('qiniu', 'sk', value='your QiNiu Secret Key')
    config.set('qiniu', 'url', value='your http prefix')
    config.set('qiniu', 'bucket', value='your Bucket')
    config.write(open(config_file, 'w'))

    return config

def register(config):
    """
    Params:
        config: qiniu config
    """

    global ak, sk, url, bucket

    ak = config.get('qiniu', 'ak')
    sk = config.get('qiniu', 'sk')
    url = config.get('qiniu', 'url')
    bucket = config.get('qiniu', 'bucket')

    # authenticate
    ret = os.system('./bin/qshell account {} {}'.format(ak, sk))

    if ret == 0:
        print('Register Success!')
    else:
        raise Exception('Register Error')

def upload_to_qiniu(filename, file_path, config):
    """
    Params:
        filename: local filename
        file_path: target file path
        config: qiniu config
    Return:
        Uploaded url on QiNiu
    """

    global url, debug

    # upload
    if debug:
        ret = subprocess.call(['./bin/qshell', 'fput', bucket, filename, file_path])
    else:
        dev_null = open('/dev/null', "w")
        ret = subprocess.call(['./bin/qshell', 'fput', bucket, filename, file_path], stdout=dev_null, stderr=dev_null)
        dev_null.close()

    if ret == 0:
        _url = os.path.join(url, filename)
        print('{} -> {} Uploaded.'.format(file_path, _url))
        return _url
    else:
        raise Exception('Error')

def read_config():
    config_dir = os.path.join(os.environ['HOME'], '.qiniu')
    config_path = os.path.join(config_dir, 'qiniu_config.ini')

    # if config file not exist, make blank one
    if not os.path.exists(config_path):
        print('Config file not found, making blank config file to `{}`'.format(config_path))
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)
        make_blank_config(config_path)
    
    config = configparser.RawConfigParser(allow_no_value=True)
    config.read(config_path)