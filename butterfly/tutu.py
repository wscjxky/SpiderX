# -*- coding: utf-8 -*- #
import os

import re
import xlrd


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


def walks():
    for (root, dirs, files) in os.walk('D:/tutu'):
        files_list = []
        for i in dirs:
            for (root1, dirs1, files1) in os.walk('D:/tutu/' + i):
                files_list = files1
            dir_name = i.decode('gbk')
            file_name = i.decode('gbk')
            print file_name
            genDictByPhone('list.xlsx', dir_name, files_list)
            0

# txt_list=[]
# with open('all.txt', 'r') as f:
#     lines = f.readlines()
#     for l in lines:
#         txt= re.search('(.+)_', l).group(1)
#         txt_list.append(txt)
# txt_list=set(txt_list)
#
# dic=''
# index=1
# with open('results.txt','a') as f:
#     for key,value in enumerate(txt_list):
#         dic=''
#         print key
#         dic+='item { \n'
#         dic+='  id: ' + str(index) +'\n'
#         dic+='  name: \'' +value +'\'\n'
#         dic+='}\n'
#         f.write(dic)
#         index+=1
# print dic

if __name__ == '__main__':
    for roots,dirs,files in os.walk('F:/tutu/out'):
        for fil in files:
            with open('F:/tutu/out/'+fil, 'rb') as f:
                with open('new_out/'+fil, 'a') as f1:
                    j = 0
                    for i in f.readlines():
                        if j == 0:
                            j += 1
                            continue
                        f1.write(i)

                        wrong = 0


                        def same(example, list):
                            example = example.lower()
                            for i in list:
                                diff = 0
                                if len(i) == len(example):
                                    for j in range(len(example)):
                                        if example[j] == i[j]:
                                            diff += 0
                                        else:
                                            diff += 1
                                    if diff > 1:
                                        continue
                                    if diff == 1:
                                        return i, 1
                                        # if diff==2:
                                        #     return i,1
                            return example, 0


                        num = int(input())
                        str = input()
                        str = str.replace("!", " ")
                        str = str.split(" ")
                        word = []
                        pr = []
                        for i in range(num):
                            word.append(input())
                        for i in str:
                            sout = same(i, word)
                            pr.append(sout[0])
                            wrong += sout[1]
                        print(wrong)
                        print(pr[0].title(), end=' ')
                        for i in range(1, len(str) - 2):
                            print(pr[i], end=" ")
                        print(pr[len(str) - 2] + "!")

    # dic=''
    # index=1
    # xls_file='list.xlsx'
    # wb = xlrd.open_workbook(xls_file)
    # sheet = wb.sheet_by_index(0)
    # with open('results.txt','a') as f:
    #     for irow in range(sheet.nrows):
    #         c_row = sheet.row(irow)
    #         value = c_row[0].value
    #         name = c_row[1].value
    #         dic = ''
    #         dic += 'item { \n'
    #         dic += '  id: ' + str(index) + '\n'
    #         dic += '  name: \'' + name + '\'\n'
    #         dic += '}\n'
    #         f.write(dic)
    #         index += 1

