from pythonfile import merged
import time
import subprocess
import json
import os.path
import sys
import datetime


def runSentiment(path):
    os.chdir(path+'\\pythonfile\\')
    subprocess.Popen([sys.executable, "merged.py"])
    subprocess.Popen([sys.executable, "sentiment.py"])

##############################################################################################################


def runScrapy(path):
    subprocess.Popen([r''+path+'\\run.bat'])
    os.chdir(path+'\\virtual_env\\demo_project\\')
    subprocess.run(["scrapy", "crawl", "oilnews"])

##############################################################################################################


def main():
    path = str(sys.path[0])
    runScrapy(path)
    runSentiment(path)
    print("Done")

##############################################################################################################
main()
