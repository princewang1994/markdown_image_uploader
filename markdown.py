import re
import os
import copy
import argparse
import traceback
from upload.upload import UploadFilter
from backup.backup import BackupFilter
from util import make_filename, get_par_dir, compress_image
from PIL import Image

# markdown image regex
md_img_re = r'\!\[.*\]\((.*?)\)'

def main(args):

    # initialize filter
    if args.cmd == 'upload':
        print('Uploading `{}` with method: {}'.format(args.md_path, args.method))
        md_img_filter = UploadFilter(args)    
    else:
        print('Backuping `{}` to {}'.format(args.md_path, args.backup_dir))
        md_img_filter = BackupFilter(args)

    # read markdown text
    with open(args.md_path, 'r') as f:
        text = f.read()
        ori_text = copy.copy(text)

    # get parent dir
    parent_path = get_par_dir(args.md_path)

    # find all markdown image in text
    md_imgs = re.findall(md_img_re, text)

    # output all images in markdown
    print('Finding Images in {}'.format(args.md_path))
    if len(md_imgs):
        print('{} images found:'.format(len(md_imgs)))
        for img in md_imgs:
            print('-> {}'.format(img))
    else:
        print('No images to deploy')
        exit(0)
    
    print('Operating.')
    try: # if there is any image to be filt 
        
        for md_img in md_imgs:
            text = md_img_filter.filter(md_img, text, parent_path)

        # if there are images changes
        if text != ori_text:
            print('complete, writing back to {} ...'.format(args.md_path))
            # write back
            with open(args.md_path, 'w') as f:
                f.write(text)
            print('Complete')
        else:
            print('No change, finish.')

    # if there is any exception, write back original text
    except Exception: 
        print('Unknown error')
        if args.debug:
            traceback.print_exc()
        with open(args.md_path, 'w') as f:
            f.write(ori_text)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', type=str, choices=['backup', 'upload'], help='Command')
    parser.add_argument('md_path', type=str, help='Markdown file path')
    parser.add_argument('-d', '--debug', action='store_true', help='Debug mode')
    
    # Upload Options
    parser.add_argument('--method', type=str, default='ali', help='Markdown file path')
    
    # Backup Options
    parser.add_argument('--dst', dest='backup_dir', type=str, default='./backup_img', help='Backup')
    
    args = parser.parse_args()
    main(args)
