from requests_html import HTMLSession
import requests
import sys
robclass_headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/74.0.3729.169 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'
                    }
def download(download_link, title):
    r = requests.get(download_link,headers=robclass_headers)
    print(r.content)
    with open(title+".pdf", "wb") as f:
        for chunk in r.iter_content(chunk_size=512):
            f.write(chunk)
# download("http://resources.metmuseum.org/resources/metpublications/pdf/Abbot_Suger_and_Saint_Denis.pdf","asdasd")
# exit()
pdf_url='http://resources.metmuseum.org/resources/metpublications/pdf/'
fs=open("book.txt",'w',encoding="utf8")
for page in range(1,51):
    url = 'https://www.metmuseum.org/art/metpublications/titles-with-full-text-online?&isappinstalled=0&from=timeline&searchtype=F&&rpp=12&pg='+str(page)
    session = HTMLSession()
    print(url)
    r = session.get(url)
    titles = r.html.find('#titleLabel')
    for t in titles:
        title=t.text
        title=title.replace(" ","_").replace("-","_").replace("–","_").replace(":","_").replace(",","_").replace("__","_")
        download_link=pdf_url+title+".pdf"
        try:
            print(download_link)
            # download(download_link,title)
            fs.write(download_link+"\n")
        except Exception as e:
            print(e)
            pass
    # for p in pages