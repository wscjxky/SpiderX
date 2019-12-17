from bs4 import BeautifulSoup
import  re
kecheng_code = ['80L342Q']
xuhao = ['01']
import  requests
with open("a.html", 'r', encoding="utf-8") as f:
    res = f.read()
    soup = BeautifulSoup(res, 'html.parser')
    table = soup.find('table', class_='table')
    class_trs = table.find_all('tr')[1:]
    for tr in class_trs:
        for index_kecheng, k_code in enumerate(kecheng_code):
            if k_code in tr.text:
                has_free = tr.find('input')
                if has_free:
                    class_code = has_free["value"].strip()
                    class_name = tr.find('div', class_='ellipsis')
                    if class_name:
                        class_name = class_name.text.strip()
                    else:
                        class_name = tr.find('div', class_='hide').text.strip()
                    class_name = re.search("】(.*)", class_name).group(1)
                    if xuhao[index_kecheng] in class_name:
                        print("有课余量：")
                        try:
                            import winsound
                            duration = 1000  # millisecond
                            freq = 500  # Hz
                            winsound.Beep(freq, duration)
                        except:
                            import os

                            duration = 1  # second
                            freq = 500  # Hz
                            os.system(
                                'play --no-show-progress --null --channels 1 synth %s sine %f' % (
                                    duration, freq))
                        print(class_name)
                        print(class_code)

