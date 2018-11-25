import re
import os
from util import file_exist
from util import make_filename, compress_image, is_image_format

class UploadFilter(object):

    def __init__(self, args):
        if args.method == 'ali':
            from .oss import upload_to_oss as upload, read_config 
        else:
            from .qiniu import upload_to_qiniu as upload, read_config
        self.args = args
        self.upload = upload
        self.read_confg = read_config
        self.config = read_config()

    def filter(self, md_img, text, parent_path):
        ori_img = md_img
        md_img = md_img.replace('%20', ' ')        
        path = os.path.join(parent_path, md_img)

        if file_exist(self.args.md_path, md_img) and is_image_format(md_img):
            print('Uploading `{}`'.format(path))
            path = compress_image(path)
            filename = make_filename(path, self.args.debug)
            url = self.upload(filename, path, self.config)
            text = text.replace(ori_img, url)
        else:
            print('{} -> no need to upload'.format(md_img))
        
        return text