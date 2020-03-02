from pythainlp.tokenize import word_tokenize
from datetime import datetime
from pandas import DataFrame
from dateutil.parser import parse
from itertools import groupby
from collections import Counter
# from loguru import logger

import re
import xlrd
import json
import sorting
import time
import numpy
import sys
import nltk
import itertools
import os.path

# //declare value
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
keyword = [];
dates = [];
increase_key = [];
decrease_key = [];
impactWord = [];
w,h = 0,0;
news = [[0 for x in range(w)] for y in range(h)]
table = [[0 for x in range(w)] for y in range(h)]

now = datetime.now()
dateTime = now.strftime("%Y-%m-%d %H.%M.%S")
#################################################################################################
def insert_table(indexNews,date,trend,amount):
    
    # ถ้าเคยมีวันที่อยู่ใน list จะทำการบวกเพิ่มในคอลัมน์ที่ระบุ
    # เมื่อ indexTrend = 1 คือ increase และ 2 คือ decrease
    if indexNews < len(table):
        table[indexNews][trend] += amount 
        return True
    
    # ถ้ายังไม่เคยมีวันที่ จะทำการเพิ่ม list ของวันที่นั้นต่อท้าย
    # รูปแบบ ['2019-01-01',0,0]
    # โดย 0,0 คือ ค่าผลรวมของ increase และ decrease ตามลำดับ
    zeros = [0,0];
    table.insert(len(table),[date]+zeros);
    table[len(table)-1][trend] += amount;

    return True
#################################################################################################
def readFileDictionary(file):
    wd = xlrd.open_workbook(file)
    sheet = wd.sheet_by_index(0)
    sheet.cell_value(0,0)

    for i in range(1,sheet.nrows):
        if(sheet.cell_value(i,1) != ''):
            temp = sheet.cell_value(i,1).lower().split(' ');
            keyword.insert(i,temp);
    
    for i in range(1,sheet.nrows):
        if(sheet.cell_value(i,2) != ''):
            increase_key.insert(i,sheet.cell_value(i,2).lower());
        
    for i in range(1,sheet.nrows):
        if(sheet.cell_value(i,3) != ''):
            decrease_key.insert(i,sheet.cell_value(i,3).lower());
    
    for i in range(1,sheet.nrows):
        if(sheet.cell_value(i,4) != ''):
            impactWord.insert(i,sheet.cell_value(i,4).lower())
    
    return True
#################################################################################################
def readFileNews():
    with open(os.path.abspath('virtual_env\demo_project\\news.json')) as filenews:
        sheet = json.load(filenews)

    for i in range (len(sheet['title'])):
        tmp_title = sheet['title'][i].lower();
        tmp_content = sheet['content'][i].lower();
        tmp_date = sheet['date'][i].split(" ",1)[0];
        
        f3 = open("file\\apostrophe-lower.txt","r")
        for line3 in f3:
            words3 = line3.split(",")
            tmp_title = tmp_title.replace(words3[1].strip().lower(),words3[0].lower())
            tmp_content = tmp_content.replace(words3[1].strip().lower(),words3[0].lower())
        
        news.insert(i-1,[tmp_title,tmp_content,tmp_date]);
        

    news.sort(key=lambda x: x[2]);

    for i in range(len(news)):
        dates.append(news[i][2]);  
      
    dates.insert(0,'date')
    return True
#################################################################################################
def findWord(sentence,word):
    if sentence.find(' '+word) == -1 and sentence.find(' '+word+' ') == -1 and sentence.find(word+' ') == -1:
        return -1
    elif sentence.find(' '+word+' ') != -1 or sentence.find(word+' ') == 0 or sentence.find(' '+word)+len(word) == len(sentence):
        return sentence.find(' '+word+' ') + len(word)+1
    else:
        return -1

#################################################################################################
def cutKum(trend): 
    # trend บอกพจนานุกรมของแนวโน้มราคาน้ำมัน (1 คือ แนวโน้มเพิ่มขึ้น)(2 คือแนวโน้มลดลง)
    if trend == 1:
        present_key = increase_key;
    else:
        present_key = decrease_key;
    

    count = 0

    # ทำการอ่านแต่ละข่าว
    for iNews in news:
        count+=1;
        date = iNews[2];
        iNews[1] = iNews[1].replace('[\'','').replace('\']','').replace(', ','').replace('\'\'',' ')
        
        # รวมหัวเรื่องข่าวกับเนื้อหาข่าวให้อยู่ใน content เดียวกัน
        mixNews = iNews[0]+'. '+iNews[1];
        content = nltk.sent_tokenize(mixNews)
        tempKey = [];
        
        # วนอ่านแต่ละ sentense ใน content
        for sentense in content:
            # วนอ่่านแต่ละ key ใน พจนานุกรมแนวโน้มราคาน้ำมัน
            # เรียกแทนว่า dialog 
            for dialog in present_key:
                isMatch = True
                subSen = sentense
                
                #กรณีมี dialog ที่เคยเจอแล้ว
                #ให้ข้าม ไป ยัง dialog ถัดไป
                if dialog in tempKey:
                    continue

                # ทำการตัด dialog ให้อยู่ในรูปอาเรย์ ในชื่อตัวแปร subDialog
                # เพื่อรองรับกรณี dialog ที่เป็นกลุ่มคำ เช่น turn on
                subDialog = dialog.split(" ")
               
                # วนอ่านแต่ละคำใน dialog
                for iWord in subDialog:
                    
                    # กรณีไม่พบส่วนหนึ่งของ dialog แสดงว่าไม่มี key นั้นอยู่ในประโยค
                    if findWord(subSen.translate(non_bmp_map), iWord) == -1:
                       isMatch = False
                       break
                    # กรณีพบส่วนหนึ่งของ dialog
                    # จะให้ทำการตัดประโยคนั้นให้เหลือเฉพาะส่วนที่ยังไม่ได้อ่าน
                    else:
                       tempIndex = findWord(subSen.translate(non_bmp_map),iWord)
                       subSen = subSen[tempIndex:]

                # เมื่ออ่าน dialog แล้ว
                # สถานะ isMatch จะบอกว่า key นั้นปรากฎใน sentense หรือเปล่า
                if isMatch:
                    tempKey.append(dialog);
        
        insert_table(count-1,date,trend,len(tempKey));
        
    return True
#################################################################################################
def toExcel():
    title = []
    date = []
    increase_word = []
    decrease_word =[] 
    total = []
    increase = []
    decrease = []
    trend = []
    
    for i in range(len(news)):
        title.append(news[i][0]);

    for i in range(len(table)):
        date.append(table[i][0]);
        increase_word.append(table[i][1]);
        decrease_word.append(table[i][2]);
        total.append(table[i][1]+table[i][2])
        if table[i][1]+table[i][2] != 0:
            increase.append(table[i][1]/(table[i][1]+table[i][2]))
            decrease.append(table[i][2]/(table[i][1]+table[i][2]))
            trend.append((table[i][1]/(table[i][1]+table[i][2])) - (table[i][2]/(table[i][1]+table[i][2])))
        else:
            increase.append(0)
            decrease.append(0)
            trend.append(0)

    data = {
        "title":title,
        "date": date,
        "increase_word": increase_word,
        "decrease_word":decrease_word,
        "total":total,
        "increase":increase,
        "decrease":decrease,
        "trend" : trend,
    }
    excel = json.dumps(data)

    df =  DataFrame(data,columns=data.keys())
    export_excel = df.to_excel (r'C:\Users\supak\Desktop\scrpy\scrapy_simple\result\result_'+dateTime+'.xlsx', index = None, header=True)
    
    
#################################################################################################
def main():
    
    start = datetime.now()
    file1 = "file\DictionaryOil_270220.xlsx"
    readFileDictionary(file1)
    readFileNews()

    cutKum(1)
    cutKum(2)
    sorted(table, key=lambda t: t[0])
    toExcel()

main()