import os
import time
import random
import re
from PIL import Image
import errno

def mkdirs(newdir):
    try: 
        os.makedirs(newdir)
    except OSError as err:
        # Reraise the error unless it's about an already existing directory 
        if err.errno != errno.EEXIST or not os.path.isdir(newdir): 
            raise

def file_exist(md_path, path):
    """
        Check file path exists in:
        - absolute path
        - current/path
    """
    if os.path.exists(path): 
        return True
    par_path = os.path.dirname(md_path)
    path = os.path.join(par_path, path)
    if os.path.exists(path):
        return True
    return False

def is_image_format(path):
    # valid image postfix
    types = ['png', 'jpg', 'jpeg', 'gif']
    img_postfix_re = '\.' + '|'.join(types) + '$'
    return re.findall(img_postfix_re, path)

def make_filename(old_filename, debug=False):
    file_typle = os.path.basename(old_filename).split('.')[-1]
    prefix = 'debug' if debug else 'blog'
    rnd = random.randint(0, 999)
    return prefix + '_' + time.strftime('%Y%m%d%H%M%S') + '%04d' % rnd + '.' + file_typle

def get_par_dir(path):

    basename = os.path.basename(path)
    path = path[:-len(basename)]

    if path == '':
        return '.'
    else:
        return path

def compress_image(path, thresh=0.2):
    """Compress Image
    """
    
    file_stat = os.stat(path)
    basename = os.path.basename(path)
    file_type = basename.split('.')[-1]

    # dont compress gif file
    if file_type == 'gif':
        return path

    file_size = file_stat.st_size / 1024.**2
    # if file is larger than 200k
    if file_size > 0.2:
        print('Image `{}` is larger than 200k({:.2}m), need to compress.'.format(path, file_size))
        import tempfile
        temp_dir = tempfile.gettempdir()

        img = Image.open(path)
        H, W = img.size
        if H > W:
            w = int(thresh * 2048 * 2)
            h = int(H * w / W)
        else:
            h = int(thresh * 2048 * 2)
            w = int(W * h / H)

        new_path = os.path.join(temp_dir, 'compress_' + basename)
        img.resize((h, w)).save(new_path)

        return new_path
    else:
        return path