from pythainlp.tokenize import word_tokenize
from datetime import datetime
from dateutil.parser import parse
from itertools import groupby
from collections import Counter
from openpyxl import load_workbook

import re
import xlrd
import json
import sorting
import time
import numpy as np
import sys
import nltk
import itertools
import os.path
import pandas as pd

keyword = []
increase_key = []
decrease_key = []
dates = []
w, h = 0, 0
news = [[0 for x in range(w)] for y in range(h)]
table = [[0 for x in range(w)] for y in range(h)]
data = {}

now = datetime.now()
dateTime = now.strftime("%Y-%m-%d %H.%M.%S")
#################################################################################################
#################################################################################################


def invertTable(trend):
    if(trend == 1):
        present_key = increase_key
        pre_word = "increase"
    else:
        present_key = decrease_key
        pre_word = "decrease"

    data = {}
    header = [dates[0]]
    data[dates[0]] = []
    temp = []
    for i in range(len(present_key)):
        header.append(present_key[i])
        data[header[i+1]] = []

    for j in range(1, len(table[0])):
        data[dates[0]].append(dates[j])
        temp = []
        for i in range(len(table)):
            if table[i][0] not in present_key:
                continue
            else:
                if table[i][0] not in temp:
                    data[table[i][0]].append(table[i][j])
                    temp.append(table[i][0])

    for i in range(len(present_key)):
        if len(data[present_key[i]]) == 0:
            for j in range(len(dates)-1):
                data[present_key[i]].append(0)

    excel = json.dumps(data)
    if trend == 1:
        path = r'C:\\Users\\supak\\Desktop\\scrpy\\scrapy_simple\\result\\export_' + dateTime+'.xlsx'
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        df = pd.DataFrame(data, columns=data.keys())
        df.to_excel(writer, sheet_name=pre_word)
        writer.save()
        writer.close()
    else:
        path = r'C:\\Users\\supak\\Desktop\\scrpy\\scrapy_simple\\result\\export_' + dateTime+'.xlsx'
        book = load_workbook(path)
        writer = pd.ExcelWriter(path, engine='openpyxl')
        writer.book = book
        df = pd.DataFrame(data, columns=data.keys())
        df.to_excel(writer, sheet_name=pre_word)
        writer.save()
        writer.close()

#################################################################################################
#################################################################################################


def insert_table(word, indexDate):

    for i in range(len(table)):
        if word == table[i][0]:
            table[i][indexDate] = 1

    zeros = []
    zeros = zeros + [0]*(len(dates)-1 - len(zeros))
    table.insert(len(table), [word]+zeros)
    table[len(table)-1][indexDate] += 1

    return True
#################################################################################################
#################################################################################################


def readFileDictionary(file):

    wd = xlrd.open_workbook(file)
    sheet = wd.sheet_by_index(0)
    sheet.cell_value(0, 0)

    for i in range(1, sheet.nrows):
        if(sheet.cell_value(i, 1) != ''):
            temp = sheet.cell_value(i, 1).lower().split(' ')
            keyword.insert(i, temp)

    for i in range(1, sheet.nrows):
        if(sheet.cell_value(i, 2) != ''):
            increase_key.insert(i, sheet.cell_value(i, 2).lower())

    for i in range(1, sheet.nrows):
        if(sheet.cell_value(i, 3) != ''):
            decrease_key.insert(i, sheet.cell_value(i, 3).lower())
    return True
#################################################################################################
#################################################################################################


def readFileNews():
    with open(os.path.abspath('C:\\Users\\supak\\Desktop\\scrpy\\scrapy_simple\\virtual_env\\demo_project\\news.json')) as filenews:
        sheet = json.load(filenews)

    for i in range(len(sheet['title'])):
        tmp_title = sheet['title'][i].lower()
        tmp_content = sheet['content'][i].lower()
        tmp_date = sheet['date'][i].split(" ", 1)[0]

        f3 = open(
            "C:\\Users\\supak\\Desktop\\scrpy\\scrapy_simple\\file\\apostrophe-lower.txt", "r")
        for line3 in f3:
            words3 = line3.split(",")
            tmp_title = tmp_title.replace(
                words3[1].strip().lower(), words3[0].lower())
            tmp_content = tmp_content.replace(
                words3[1].strip().lower(), words3[0].lower())

        news.insert(i-1, [tmp_title, tmp_content, tmp_date])

    news.sort(key=lambda x: x[2])

    for i in range(len(news)):
        dates.append(news[i][2])

    dates.insert(0, 'date')
    return True
#################################################################################################
#################################################################################################


def findWord(sentence, word):
    if sentence.find(' '+word) == -1 and sentence.find(' '+word+' ') == -1 and sentence.find(word+' ') == -1:
        return -1
    elif sentence.find(' '+word+' ') != -1 or sentence.find(word+' ') == 0 or sentence.find(' '+word)+len(word) == len(sentence):
        return sentence.find(' '+word+' ') + len(word)+1
    else:
        return -1

#################################################################################################
#################################################################################################


def cutKum(trend):
    if trend == 1:
        present_key = increase_key
    else:
        present_key = decrease_key

    count = 0

    # ทำการอ่านแต่ละข่าว
    for iNews in news:
        count += 1
        index_date = dates.index(iNews[2])
        iNews[1] = iNews[1].replace('[\'', '').replace(
            '\']', '').replace(', ', '').replace('\'\'', ' ')

        # รวมหัวเรื่องข่าวกับเนื้อหาข่าวให้อยู่ใน content เดียวกัน
        mixNews = iNews[0]+'. '+iNews[1]
        content = nltk.sent_tokenize(mixNews)
        tempKey = []

        # วนอ่านแต่ละ sentense ใน content
        for sentense in content:
            # วนอ่่านแต่ละ key ใน พจนานุกรมแนวโน้มราคาน้ำมัน
            # เรียกแทนว่า dialog
            for dialog in present_key:
                isMatch = True
                subSen = sentense

                # กรณีมี dialog ที่เคยเจอแล้ว
                # ให้ข้าม ไป ยัง dialog ถัดไป
                if dialog in tempKey:
                    continue

                # ทำการตัด dialog ให้อยู่ในรูปอาเรย์ ในชื่อตัวแปร subDialog
                # เพื่อรองรับกรณี dialog ที่เป็นกลุ่มคำ เช่น turn on
                subDialog = dialog.split(" ")

                for iWord in subDialog:

                    if findWord(subSen, iWord) == -1:
                        isMatch = False
                        break
                    else:
                        tempIndex = findWord(subSen, iWord)
                        subSen = subSen[tempIndex:]

                if isMatch:
                    tempKey.append(dialog)
                    insert_table(str(dialog), index_date)

    return True
#################################################################################################
#################################################################################################


def main():
    start = datetime.now()
    dictionaryFile = "C:\\Users\\supak\\Desktop\\scrpy\\scrapy_simple\\file\\DictionaryOil_270220.xlsx"
    readFileDictionary(dictionaryFile)
    readFileNews()
    cutKum(1)
    sorted(table, key=lambda t: t[0])
    invertTable(1)

    cutKum(2)
    sorted(table, key=lambda t: t[0])
    invertTable(2)


main()
