import os
from aip import AipOcr
client = AipOcr("18075034", "GcBPfVEhCu6vXtEK1Qgu5wTL",
                "YeDKFlWFCwZ84DWallNL4d3u9BUTmq1V")
""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


dir1 = "D:/pycharmproject/SpiderX/robclass/t.jpg"
image = get_file_content(dir1)
res = client.basicAccurate(image)
print(res)
files = [1]
# files=os.listdir(dir1)
with open("题目2.txt", 'w', encoding="utf8") as f_w:
    for f in files:
        # image = get_file_content(dir1+"/"+f)
        # """ 调用通用文字识别, 图片参数为本地图片 """
        res = client.basicAccurate(image)
        print(res)
        for r in res['words_result']:
            word = r["words"].replace("□", "").replace("口", "")
            f_w.write(word+"\n")
            if "答案:" in word:
                f_w.write("\n")
            elif "答:" in word:
                f_w.write("\n")
