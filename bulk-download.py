from bs4 import BeautifulSoup as bs
from io import BytesIO
import requests
import zipfile
import os

FILE_LOCATIONS = ['fumen/arcade/', 'fumen/easy/', 'fumen/custom/', 'fumen/other/']
PROGRESS_FILE = 'bulk-download-progress.csv'
SKIP = -1
ARCADE = 0
EASY = 1
CUSTOM = 2
OTHER = 3

def __main__():
    completed = []
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            completed.append(f.read().split('\n'))

    setup()

    progress = open(PROGRESS_FILE, 'w')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    with open('links.csv') as flinks:
        for line in flinks:
            # If the file has been downloaded before, skip it
            if line in completed:
                continue
            title, comment, downloads, size_mb, url = line.split('|')
            print('Processing:', title, url, comment, downloads)
            try:
                with requests.Session() as session:
                    session.headers.update(headers)
                    r = session.get(url)
                    soup = bs(r.content)
                    post_data = {'token': soup.find('form', {'name': 'agree'}).input.get('value')}
                    response = session.post(url, data=post_data)
                    dl_link = bs(response.content).find('a', {'class': 'download'}).get('href')
                    dl = session.get(dl_link, stream=True)

                    zfile = zipfile.ZipFile(BytesIO(dl.content))
                    status = process(zfile, comment, downloads)

                    dirname = FILE_LOCATIONS[status] + title
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)
                    for f in zfile.infolist():
                        ext = f.filename.split('.')[-1]
                        data = zfile.read(f)
                        with open(dirname + '/' + title + '.' + ext, 'wb') as fw:
                            fw.write(data)
                    progress.write(line + '\n')

            except Exception as e:
                print('Error encountered while processing', title)
                print(e)
                import sys
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                import pdb
                pdb.set_trace()

    progress.close()

def setup():
    for f in FILE_LOCATIONS:
        if not os.path.exists(f):
            os.makedirs(f)

def process(zfile, comment, downloads):
    if '新AC' in comment:
        return ARCADE
    if int(downloads) < 2000:
        return SKIP
    with open(zfile.namelist()[1], 'r') as f:
        for line in f:
            if line.startswith('LEVEL'):
                stars = int(line.split(' ')[1])
                if stars < 7:
                    return EASY
            break
    if '創作' in comment:
        return CUSTOM
    return OTHER

if __name__ == '__main__':
    __main__()