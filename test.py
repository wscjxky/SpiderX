import re
from bs4 import BeautifulSoup

with open('test.html', 'r', encoding='utf8')as f:
    res = f.read()
from requests_html import HTMLSession
# session = HTMLSession()
# r = session.get('http://localhost:63342/SpiderX/test.html?_ijt=lotkf5mv9smj0gf5iutlntbpgq')
# r.html.render()
soup = BeautifulSoup(res, 'html.parser')
table=soup.find('div',id='current')
class_trs=table.find_all('tr')[1:]
for tr in class_trs:
    # print(tr.find('input'))
    if "85L074T" in tr.text:
        has_free = tr.find('input')
        if has_free:
            class_code = has_free["value"].strip()
            class_name = tr.find('div', class_='hide').text.strip()
            class_name=re.search("】(.*)",class_name).group(1)
            if "10" in class_name:
                print(class_name)
                print(class_code)
