import requests
from requests_html import HTMLSession

robclass_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.169 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'
}


def download(download_link, title):
    r = requests.get(download_link, headers=robclass_headers)
    print(r.content)
    with open(title + ".pdf", "wb") as f:
        for chunk in r.iter_content(chunk_size=512):
            f.write(chunk)

import os
def rename(id):
    session = HTMLSession()
    url=f'https://drive.google.com/file/d/{id}/view'
    r = session.get(url)
    title = r.html.find('title')[0].text
    if os.path.exists(f'{id}.pdf'):
        os.rename(f'{id}.pdf',f'{title}.pdf')
        print(title)


u = 'https://drive.google.com/file/d/1ssflI_6PeIBkKUtDL-14-3w-qjuLKrBo/view'
fs = open("dllinks.txt", 'r', encoding="utf8")
ls = fs.readlines()
import re

for l in ls:
    if 'drive' in l:
        id = re.findall('id=(.+)', l)
        if len(id) > 0:
            id = id[0]
            print(l)
            print(id)
            downUrl = f'https://drive.google.com/u/0/uc?id={id}&export=download'
            print(downUrl)
            # download(downUrl,id)
            rename(id)
            print(id)
