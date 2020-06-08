from pythonfile import merged
import time
import subprocess
import json
import os.path
import sys
import datetime


def runSentiment(path):
    os.chdir(path+'\\pythonfile\\')
    subprocess.Popen([sys.executable, "sentiment.py"])
    return True
##############################################################################################################


def runScrapy(path):
    subprocess.Popen([r''+path+'\\run.bat'])
    os.chdir(path+'\\virtual_env\\demo_project\\')
    subprocess.call(['ls', '-1'], shell=True)
    subprocess.run(["scrapy", "crawl", "oilnews"])

    return True
##############################################################################################################


def main():
    path = str(sys.path[0])
    runScrapy(path)
    runSentiment(path)
    return True


##############################################################################################################
main()
