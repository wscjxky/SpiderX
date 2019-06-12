table = soup.find('div', id='container')
if table:
    class_trs = table.find_all('tr')[1:]
    for tr in class_trs:
        for index_kecheng, k_code in enumerate(kecheng_code):
            if k_code in tr.text:
                has_free = tr.find('input')
                if has_free:
                    class_code = has_free["value"].strip()
                    class_name = tr.find('div', class_='hide').text.strip()
                    class_name = re.search("】(.*)", class_name).group(1)
                    if xuhao[index_kecheng] in class_name:
                        print("有课余量：")
                        print(class_name)
                        print(class_code)
                        res = requests.get('https://dean.bjtu.edu.cn/captcha/refresh/', cookies=cookies,
                                           headers=headers_image)
                        json_data = res.json()
                        hashkey = json_data['key']
                        print(json_data)
                        img_data = requests.get('https://dean.bjtu.edu.cn' + json_data['image_url'],
                                                headers=headers)
                        if pred_type == 'pp':
                            pred_type = 'pp'
                            answer, req_id = api.Predict(40300, img_data.content)
                        else:
                            pred_type = 'cjy'
                            answer, req_id = chaojiying.PostPic(img_data.content, 2003)
                        result = post_request(cookies=cookies, class_code=class_code, hashkey=hashkey,
                                              answer=answer,
                                              req_id=req_id, pred_type=pred_type)
                        if result == 200:
                            return True