# -*- coding: utf-8 -*- #
import os
import xlrd

ZhonghuanXiaDie = '中环蛱蝶'
YunBaoXiaDie = '云豹蛱蝶'
LiangHuiDie = '亮灰蝶'
YangMeiXianXiaDie = '扬眉线蛱蝶'
PeiBaoXiaDie = '斐豹蛱蝶'
MuNvZhenYanDie = '牧女珍眼蝶'
XianHuiDie = '线灰蝶'
XunMaXiaDie = '荨麻蛱蝶'
LanFengDie = '蓝凤蝶'
SheMuHeYanDie = '蛇目褐蚬蝶'
YinBanBaoDie = '银斑豹蛱蝶'
HuangGouXiaDie = '黄钩蛱蝶'


def genDictByPhone(xls_file, keyword, files_list):
    wb = xlrd.open_workbook(xls_file)
    sheet = wb.sheet_by_index(0)
    for irow in range(sheet.nrows):
        c_row = sheet.row(irow)
        try:
            value = c_row[0].value
            name = c_row[1].value
            if keyword in value:
                for i in files_list:
                    index = str(i)
                    os.rename('D:/tutu/' + value + '/' + index, 'D:/tutu/' + '/' + value + '/' + name + '_add' + index)
        except Exception as e:
            print e


for (root, dirs, files) in os.walk('D:/tutu'):
    files_list = []
    for i in dirs:
        for (root1, dirs1, files1) in os.walk('D:/tutu/' + i):
            files_list = files1
        dir_name = i.decode('gbk')
        file_name = i.decode('gbk')
        print file_name
        genDictByPhone('list.xlsx', dir_name, files_list)
