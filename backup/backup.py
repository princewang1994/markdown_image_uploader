import requests
import os
from util import file_exist, mkdirs
import shutil


class BackupFilter(object):

    def __init__(self, args):
        self.args = args
        self.backup_dir = args.backup_dir
        mkdirs(self.backup_dir)

    def filter(self, md_img, text, parent_path):
        dst_path = os.path.join(self.backup_dir, os.path.basename(md_img))
        # if local, copy to backup
        if file_exist(self.args.md_path, md_img):
            print('`{}` in local system, copy to {}'.format(md_img, dst_path))
            if os.path.exists(md_img): # absolut path
                src_path = md_img
            else: # relative path
                src_path = os.path.join(parent_path, md_img)
            shutil.copy(src_path, dst_path)
        # if url
        else:
            url = md_img
            ret = requests.get(url)
            if ret.status_code == 200:
                open(dst_path, 'wb').write(ret.content)
            else:
                print('Cannot solve `{}`.'.format(md_img))
        return text