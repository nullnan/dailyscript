#!/usr/bin/env python3
from bs4 import BeautifulSoup as bs
import bs4,time,os,requests

global url
global content
global videolist

class Episode(object):
    def __init__(self,Name,Link):
        self.Name = Name
        self.Link = Link

def DevMode():
    global content
    content = object()
    with open('dev.html','r') as file:
        content = file.read()

def getContent():
    global content
    content = requests.get(url)


def getVideoList():
    global videolist,content
    videolist = list()
    phtml = bs(content.text,'html.parser')
    # print(phtml.prettify())
    filetable = phtml.find('tbody')
    for EpisodeInfo in filetable.contents[3::2]:
        Info = [item for item in EpisodeInfo.contents if not isinstance(item,bs4.element.NavigableString)]
        # print(Info)
        videolist.append(Episode(Info[0].get_text(),Info[2].a['href']))
                

def confirm(): 
    print('There are %s Episode Fonud!' % len(videolist))
    ans = input('Download Now ? [Y/N] ')
    if ans == 'Y':
        return True
    else :
        return False

def downloadVideo():
    FileList = ''
    for video in videolist : 
        FileList += '\n%s\n out=%s'% (video.Link , video.Name)

    with open('_FileList.txt','w') as f:
        f.write(FileList)

    ret = os.system('aria2c -x 3 --max-concurrent-downloads=2 --input-file=_FileList.txt')

    if ret == 0:
        print('Success!!!')
        exit()
    else :
        print('Failed !!!')
        exit(ret)     

if __name__ == '__main__': 
    url = 'http://yp1.yayponies.no/permalink.php?link=videos/tables/7i9'
    # DevMode()
    # url = input('Input Download Url: ')
    getContent()
    getVideoList()

    print(len(videolist))
    if confirm():
        downloadVideo()
    else:
        print('Have a nice day')
        exit()

