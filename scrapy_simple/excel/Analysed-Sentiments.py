from pythainlp.tokenize import word_tokenize
from datetime import datetime
from pandas import DataFrame
from dateutil.parser import parse
from itertools import groupby
from collections import Counter
from loguru import logger
import re
import xlrd
import json
import sorting
import time
import numpy
import sys
import nltk
import itertools

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
logger.remove()
logger.add(sys.stdout, colorize=False)
now = datetime.now()
dateTime = now.strftime("%Y-%m-%d %H.%M.%S")

min_keyword = 3
min_increse_bound = 2
min_decrese_bound = 2
keyword = []
increase_key = []
decrease_key = []
w,h = 0,0
dates = []
header =[]
news = [[0 for x in range(w)] for y in range(h)]
table = [[0 for x in range(w)] for y in range(h)]
increase_table = [[0 for x in range(w)] for y in range(h)]
decrease_table = [[0 for x in range(w)] for y in range(h)]
country_key = [[0 for x in range(w)] for y in range(h)]
trade_flows = [[0 for x in range(w)] for y in range(h)]
weight_list = []
weight_list_trade = []


def insert_table(word,indexOf,weight):
    words = ["?", "!", "(", ")", "{", "}", "'", "\"", ",", ".", ":", ";",
                 "[", "]", "…", "“", "”","^","\\r", "\\n", "\\t", "’s", "'s",
                 "/","<ul>","<li>","\\xa","=","_"]
    pattern = ['\d+','[$]','[&]','[+]','[%]','[-]','[--]','[#|//~£°–—‘]','[*<*>$]','\s[a-z]\s']
  
    replace = ""
    for w in words:
        word = word.replace(w,replace)
    for pat in pattern:
        word = re.sub(pat,replace,word)
    word = word.strip()
    if len(word) == 0:
        return
    for i in range (len(table)):
        if word == table[i][0]:
            table[i][indexOf] += (1*weight)
            return
    zeros = []
    zeros = zeros + [0]*(len(dates)-1 - len(zeros))
    table.insert(len(table),[word]+zeros)
    table[len(table)-1][indexOf] += (1*weight)

def cutKum(trend):
    
    if trend == 1:
        present_key = increase_key
    else:
        present_key = decrease_key
        
    
    count = 0
    c = 0
    for iNews in news:
        count = count+1
        logger.debug("Count {}",count)
        c +=1
        text_datetime = dates.index(iNews[2])
        mixNews = iNews[0]+' '+iNews[1]
        sentences = nltk.sent_tokenize(mixNews)
        tempKey = []
        tempCountry = []
        tempTrade = []
            
        for iSen in sentences:
            for keyCountry in country_key:
                isMatch = True
                subtences = nltk.sent_tokenize(mixNews)
                subSen = iSen
                
                for kc in keyCountry:
                    if findWord(subSen,kc) == -1 :
                        isMatch = False
                    else:
                        tempIndex = findWord(subSen.translate(non_bmp_map),kc)
                        subSen = subSen[tempIndex:]

                    if isMatch :
                        tempCountry.append([count,keyCountry[0]])
                            
            values = set(map(lambda x:x[0], tempCountry))
            newlist = [[y[1] for y in tempCountry if y[0]==x] for x in values]
 
        weight = 0.5
        for iSen in sentences:
            if len (newlist) == 0:
                weight = 0.5
            else:
                for i in newlist:
                    temp = list(set(i))
                if len(temp) == 1:
                    for w in weight_list:
                        if len(w) == 2 and w[0] == temp[0]:
                            weight = 1+w[len(w)-1]
                elif len(temp) > 1:
                    for i in trade_flows:
                        k = []
                        k.append(i[0])
                        k.append(i[1])
                        k = set(k)
                        if k.issubset(temp):
                            for j in weight_list_trade:
                                if j[0] == i[2]:
                                   weight = 1+j[1]

                        else:
                            tmp = []
                            for t in range(len(temp)):
                                for w  in weight_list:
                                    if temp[t] == w[0]:
                                        tmp.append(w[len(w)-1])
                            weight = max(tmp)
    
            
            for iDialog in present_key:
                isMatch = True
                subtences = nltk.sent_tokenize(mixNews)
                subSen = iSen
                subDialog  = iDialog.split(" ")
                for iWord in subDialog:
                    if findWord(subSen.translate(non_bmp_map),iWord) == -1 :
                        isMatch = False
                    else :
                        tempIndex = findWord(subSen.translate(non_bmp_map),iWord)
                        subSen = subSen[tempIndex:]
            
                if isMatch :
                    tempKey.append(iDialog)
                    insert_table(str(iDialog),text_datetime,weight)
                      
    return True


def readFileNews(file):
    wd = xlrd.open_workbook(file)
    sheet = wd.sheet_by_index(0)
    sheet.cell_value(0,0)

    a,b = 0,0
    check_in = []
    check_de = []
    check_key = []
    
    for i in range(1,sheet.nrows):
        tmp_title   = sheet.cell_value(i,2).lower()
        tmp_content = sheet.cell_value(i,3).lower()
        tmp_date = sheet.cell_value(i,1)
      
        f3 = open("apostrophe-lower.txt","r")
        for line3 in f3:
            words3 = line3.split(",")
            tmp_title = tmp_title.replace(words3[1].strip().lower(),words3[0].lower())
            tmp_content = tmp_content.replace(words3[1].strip().lower(),words3[0].lower())
       
        news.insert(i-1,[tmp_title,tmp_content,tmp_date])

    
    selected_date = ""
    news.sort(key=lambda x: x[2])
    
    for i in range(len(news)):
        if selected_date != news[i][2]:
            dates.append(news[i][2])    
            selected_date = news[i][2]
    dates.insert(0,'date')
    return True


def findWord(sentence,word):
    if sentence.find(' '+word) == -1 and sentence.find(' '+word+' ') == -1 and sentence.find(word+' ') == -1:
        return -1
    elif sentence.find(' '+word) != -1:
        return sentence.find(' '+word) + len(word)+1
    elif sentence.find(' '+word+' ') != -1:
        return sentence.find(' '+word+' ') + len(word)+1
    elif sentence.find(word+' ') != -1:
        return sentence.find(word+' ') + len(word)+1
    else:
        return -1

def readFileDictionary(file):
    
    wd = xlrd.open_workbook(file)
    sheet = wd.sheet_by_index(0)
    sheet.cell_value(0,0)

    for i in range(1,sheet.nrows):
        if(sheet.cell_value(i,1) != ''):
            temp = sheet.cell_value(i,1).lower().split(' ')
            keyword.insert(i,temp)
    
    for i in range(1,sheet.nrows):
        if(sheet.cell_value(i,2) != ''):
            increase_key.insert(i,sheet.cell_value(i,2).lower())
        
    for i in range(1,sheet.nrows):
        if(sheet.cell_value(i,3) != ''):
            decrease_key.insert(i,sheet.cell_value(i,3).lower())
    return True


def readFileCountry(f1,f2):
    
    wd = xlrd.open_workbook(f1)
    sheet = wd.sheet_by_index(0)
    sheet.cell_value(0,0)

    for i in range(1,sheet.nrows):
        if(sheet.cell_value(i,1) != '') and (sheet.cell_value(i,2) != ''):
            country_key.insert(i,[sheet.cell_value(i,1).lower(),sheet.cell_value(i,2).lower()])
            weight_list.append([sheet.cell_value(i,1).lower(),sheet.cell_value(i,2).lower(),sheet.cell_value(i,3)])
        else:
            country_key.insert(i,[sheet.cell_value(i,1).lower()])
            weight_list.append([sheet.cell_value(i,1).lower(),sheet.cell_value(i,3)])
        temp = []
        temp.append(sheet.cell_value(i,3))
        maximum = max(temp)

    calWeightCountry(maximum,1)

    wd = xlrd.open_workbook(f2)
    sheet = wd.sheet_by_index(0)
    sheet.cell_value(0,0)

    temp = []
    n=0
    for i in range(3,sheet.nrows):
        if(sheet.cell_value(i,0) != '') or (sheet.cell_value(i,1) != '') or (sheet.cell_value(i,2) != '') or (sheet.cell_value(i,3) != ''):
            n = n+1
            if sheet.cell_value(i,0).lower() or sheet.cell_value(i,1).lower() or sheet.cell_value(i,2).lower() or sheet.cell_value(i,3).lower() not in country_key[i]:
                country_key.insert(i,[sheet.cell_value(i,0).lower(),sheet.cell_value(i,1).lower()])
                country_key.insert(i,[sheet.cell_value(i,2).lower(),sheet.cell_value(i,3).lower()])

            trade_flows.insert(i,[sheet.cell_value(i,0).lower(),sheet.cell_value(i,2).lower(),n])
            trade_flows.insert(i,[sheet.cell_value(i,2).lower(),sheet.cell_value(i,0).lower(),n])
            weight_list_trade.append([n,sheet.cell_value(i,4)])
            weight_list_trade.append([n,sheet.cell_value(i,4)])

        
        temp.append(sheet.cell_value(i,4))
        maximum = max(temp)

    calWeightCountry(maximum,2)
    
    return True

def calWeightCountry(maximum,num):
    if num == 1:
        for w  in weight_list:
            tempWeight = w[len(w)-1]/maximum
            w[len(w)-1] = round(tempWeight, 2)
    else:
        n = 0
        for w in weight_list_trade:
            if n <= 2:
                n = n+1
                w1 = w[len(w)-1]/maximum
                w2 = w[len(w)-1]/maximum
            else:
                n = 0
            w[len(w)-1] = round(w1,2)
            w[len(w)-1] = round(w2,2)

    

    return True

def invertTable(trend):
    if(trend==1):
        present_key = increase_key
        pre_word = "increase"
    else:
        present_key = decrease_key
        pre_word = "decrease"
    
    data = {}
    header2 = [dates[0]]
    data[dates[0]] = []
    for i in range (len(table)):
        if table[i][0] not in present_key:
            continue
        data[table[i][0]] = []
        header2.append(table[i][0])


    for j in range(1,len(table[0])):
        data[dates[0]].append(dates[j])
        for i in range (len(table)):
            if table[i][0] not in present_key:
                continue
            else:
                data[table[i][0]].append(table[i][j])

    excel = json.dumps(data)

    df =  DataFrame(data,columns=data.keys())
    export_excel = df.to_excel (r'C:\Users\MiniPair\Desktop\scrpy\scrapy_simple\excel\result\export_'+pre_word+'_'+dateTime+'.xlsx', index = None, header=True)
    

def main():
    start=datetime.now()
    file1 = "DictionaryOil_271119.xlsx"
    file2 = "excel_detail(2020-02-11 16.50.20).xlsx"
    file3 = "Oil production countries_121119.xlsx"
    file4 = "TradeFlow_131119.xlsx"
    

    readFileDictionary(file1)
    readFileCountry(file3,file4)
    readFileNews(file2)

    # cutKum(1)
    # cutKum(2)
    # sorted(table, key=lambda t: t[0])
    # invertTable(1)
    # invertTable(2)


    print(datetime.now()-start)
main()
