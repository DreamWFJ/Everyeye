# -*- coding: utf-8 -*-
# ===================================
# ScriptName : download.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-11 9:51
# ===================================

import os
import xlwt
import csv
import time
import json
ezxf = xlwt.easyxf
from config import download_doc_path

def write_xls(username, file_name, sheet_name, headings, data):
    book = xlwt.Workbook()
    sheet = book.add_sheet(sheet_name)
    rowx = 0
    heading_xf = ezxf('font: bold on; align: wrap on, vert centre, horiz center')
    for colx, value in enumerate(headings):
        sheet.write(rowx, colx, value, heading_xf)
    sheet.set_panes_frozen(True) # frozen headings instead of split panes
    sheet.set_horz_split_pos(rowx+1) # in general, freeze after last heading row
    sheet.set_remove_splits(True) # if user does unfreeze, don't leave a split there
    for row in data:
        rowx += 1
        for colx, value in enumerate(row):
            sheet.write(rowx, colx, value, xlwt.easyxf())
    filename = "%s%s.xls"%(file_name, time.strftime("%Y%m%d%H%M%S"))
    user_download_doc_path = os.path.join(download_doc_path, 'excel', username)
    filename = os.path.join(user_download_doc_path, filename).replace('\\', '/')

    if not os.path.isdir(user_download_doc_path):
        os.makedirs(user_download_doc_path)
    book.save(filename)

    return filename

def write_json(username, file_name, data):
    filename = "%s%s.json"%(file_name, time.strftime("%Y%m%d%H%M%S"))
    user_download_doc_path = os.path.join(download_doc_path, 'json', username)
    filename = os.path.join(user_download_doc_path, filename).replace('\\', '/')

    if not os.path.isdir(user_download_doc_path):
        os.makedirs(user_download_doc_path)
    with file(filename, 'w') as f:
        f.write(json.dumps(data))

    return filename


def write_csv(username, file_name,headings, data):
    filename = "%s%s.csv"%(file_name, time.strftime("%Y%m%d%H%M%S"))
    user_download_doc_path = os.path.join(download_doc_path, 'csv', username)
    filename = os.path.join(user_download_doc_path, filename).replace('\\', '/')

    if not os.path.isdir(user_download_doc_path):
        os.makedirs(user_download_doc_path)
    with file(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(headings)
        writer.writerow(data)

    return filename

def write_txt(username, file_name,headings, data):
    filename = "%s%s.txt"%(file_name, time.strftime("%Y%m%d%H%M%S"))
    user_download_doc_path = os.path.join(download_doc_path, 'txt', username)
    filename = os.path.join(user_download_doc_path, filename).replace('\\', '/')

    if not os.path.isdir(user_download_doc_path):
        os.makedirs(user_download_doc_path)
    with file(filename, 'wb') as f:
        f.writelines(['  '.join(headings)])
        f.write('\n')
        f.writelines(['  '.join(map(str, one)) for one in data])

    return filename

if __name__ == '__main__':
    write_xls('test', '1', ['Data', 'ID', 'Name'], [['2012-12-15 15:35:55', '1', 'WFJ'],['2012-12-16 15:35:50', '2', 'TEST']])