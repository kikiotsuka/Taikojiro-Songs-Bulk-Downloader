from bs4 import BeautifulSoup as bs
import requests

base = ['http://ux.getuploader.com/e2339999zp/', 'http://ux.getuploader.com/e2337650/', 'http://ux.getuploader.com/toukyuutoyoko9000/', 'http://ux.getuploader.com/e2351000/']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
all_links = []

for b in base:
    print('===== SCRAPING BASE PAGE =====', b)
    for idx in range(1, 999):
        url = b + 'index/' + str(idx) + '/date/desc'
        print('=== Sub Scrape ===', url)
        base_done = False
        try:
            r = requests.get(url, headers=headers)
            html = r.content
            soup = bs(html)
            rows = soup.find_all('table', class_='table table-small-font table-hover')[0].find_all('tr')[1:]
            
            if rows:
                for row in rows:
                    link = row.a.get('href')

                    td_list = list(map(lambda x: x.contents[0].encode('utf-8'),row.find_all('td')))

                    title = row.a.get('title').encode('utf-8')
                    comment = td_list[1]
                    downloads = td_list[-2]
                    all_links.append('|'.join([title, link, comment, downloads]))
                    print(all_links[-1])
            else:
                base_done = True
        except Exception as e:
            print(e)
            base_done = True
        if base_done:
            break

with open('links.csv', 'w') as f:
    for l in all_links:
        f.write(l + '\n')