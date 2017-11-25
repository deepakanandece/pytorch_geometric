from __future__ import division

import os
import sys
from six.moves import urllib
import requests

from .dir import make_dirs
from .progress import Progress


def download_url(url, dir):
    make_dirs(dir)

    filename = url.rpartition('/')[2]
    file_path = os.path.join(dir, filename)

    try:
        response = requests.get(url, stream=True)
        size = int(response.headers.get('content-length'))
        type, div = file_type(size)
        progress = Progress('Downloading', url, round(size / div, 1), type)

        with open(file_path, 'wb') as f:
            downloaded = 0
            for data in response.iter_content(chunk_size=2**18):
                downloaded += len(data)
                f.write(data)
                progress.update(round(downloaded / div, 1))
            progress.success()
    except:
        # TODO: Ctrl-C prints character which messes with the displayed output.
        progress.fail()
        os.unlink(file_path)
        sys.exit(1)

    return file_path


def file_type(size):
    div = 1
    for type in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return type, div
        div *= 1024
        size /= 1024