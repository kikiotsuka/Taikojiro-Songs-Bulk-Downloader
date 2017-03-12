import requests
from bs4 import BeautifulSoup as bs

logging = open('bulk-download-progress.csv')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
with open('links.csv') as f:
    for line in f:
        title, comment, downloads, size_mb, link = line.split('|')
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
                with open(title, 'wb') as zip_file:
                    zip_file.write(dl.content)
                logging.print(line + '\n')
        except Exception as e:
            print('Error encountered while processing', title)
            print(e)

logging.close()