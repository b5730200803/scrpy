from pythonfile import merged
import time
import subprocess
import json
import os.path
import sys
import datetime
sys.path.insert(0, '/scrpy/scrapy_simple/pythonfile/')

def runScrapy():
    path = str(sys.path[1])
    subprocess.Popen([r''+path+'\\run.bat'])
    os.chdir(path+'\\virtual_env\\demo_project\\')
    subprocess.call(['ls', '-1'], shell=True)
    subprocess.run(["scrapy", "crawl", "oilnews"])
    subprocess.run(["scrapy", "crawl", "hellenic"])

    return True
##############################################################################################################


def main():
    runScrapy()
    return True


##############################################################################################################
main()
