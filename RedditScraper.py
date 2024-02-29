import datetime
import os
import re
import shutil
from threading import Thread
from time import sleep
from xmlrpc.client import DateTime
from praw.models import Subreddit
import requests
import praw
import configparser
import concurrent.futures
import pathlib
from Constants import * 

config = configparser.ConfigParser()
config.read(RScrConfigFile)
__SubReddit = config['REDDIT']['SubReddit']
__Quantity = config['REDDIT']['Quantity']
__Order = config['REDDIT']['Order']
__OrderTimeFilter = config['REDDIT']['OrderTimeFilter']

class redditImageScraper:
    def __init__(self, sub, limit, order, nsfw=False, test = False):
        self.sub = sub
        self.limit = (int)(limit)
        self.order = order
        self.nsfw = nsfw
        self.path = SourceDirectory
        self.reddit = praw.Reddit(client_id=config['REDDIT']['client_id'],
                                  client_secret=config['REDDIT']['client_secret'],
                                  user_agent='Multithreaded Reddit Image Downloader v2.0 (by u/impshum)')

    def download(self, image):
        print("Image downloaded!!!")
        r = requests.get(image['url'])
        with open(image['fname'], 'wb') as f:
            f.write(r.content)

    def start(self):
        images = []
        try:
            go = 0
            if self.order == 'hot':
                submissions = self.reddit.subreddit(self.sub).hot(limit=None)
            elif self.order == 'top':
                submissions = self.reddit.subreddit(self.sub).top(limit=None, time_filter = GetOrderTimeFilter())
            elif self.order == 'new':
                submissions = self.reddit.subreddit(self.sub).new(limit=None)

            print("Looking at submissions...")
            for submission in submissions:
                if not submission.stickied and submission.over_18 == self.nsfw \
                    and submission.url.endswith(('jpg', 'jpeg', 'png')):
                    fname = self.path + re.search('(?s:.*)\w/(.*)', submission.url).group(1)
                    if not os.path.isfile(fname):
                        images.append({'url': submission.url, 'fname': fname})
                        go += 1
                        if go >= self.limit:
                            break

            print("Start download...")
            if len(images):
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
                with concurrent.futures.ThreadPoolExecutor() as ptolemy:
                    ptolemy.map(self.download, images)
        except Exception as e:
            print(e)

def RedditDownload():
    try:
        ClearDirectory(LocalDerictory)
        ClearDirectory(SourceDirectory)
        scraper = redditImageScraper(__SubReddit, __Quantity, __Order)
        scraper.start()
        return True
    except:
        return False
    
def ClearDirectory(Directory):
    for filename in os.listdir(Directory):
        file_path = os.path.join(Directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
def ChangeSubreddit(NewSubreddit):
    AllGood = False
    global __SubReddit 
    try:
        scraper = redditImageScraper(NewSubreddit, __Quantity, __Order)
        AllGood = True
    except:
        AllGood = False
        
    if (AllGood):
        __SubReddit = NewSubreddit
        ChangeConfig('Subreddit', NewSubreddit)
        return True
    else:
        return False
    
def ChangeOrder(NewOrder):
    AllGood = False
    global __Order 
    try:
        scraper = redditImageScraper(__SubReddit, __Quantity, NewOrder)
        AllGood = True
    except:
        AllGood = False
        
    if (AllGood):
        __Order = NewOrder
        ChangeConfig('Order', NewOrder)
        return True
    else:
        return False
    
def ChangeOrderTimeFilter(NewOrderTimeFilter):
    AllGood = False
    global __OrderTimeFilter 
    try:
        __OrderTimeFilter = NewOrderTimeFilter
        scraper = redditImageScraper(__SubReddit, __Quantity, __Order)
        ChangeConfig('OrderTimeFilter', NewOrderTimeFilter)
        return True
    except:
        __OrderTimeFilter = config['REDDIT']['OrderTimeFilter']
        return False
  
def ChangeQuantity(NewQuantity):
    global __Quantity 
    try:
        int(NewQuantity)
        __Quantity = NewQuantity
        ChangeConfig('Quantity', NewQuantity)
        return True
    except:
        return False

def GetSubreddit():
    return __SubReddit

def GetQuantity():
    return __Quantity
    
def GetOrder():
    return __Order

def GetOrderTimeFilter():
    return __OrderTimeFilter

def ChangeConfig(Title, Value):
    config['REDDIT'][Title] = Value
    with open(RScrConfigFile, mode = "w") as configfile:
        config.write(configfile)
    config.read(RScrConfigFile)

def BackupSettings():
    global __Quantity 
    global __SubReddit
    global __Order 
    global __OrderTimeFilter
    __SubReddit = config['REDDIT']['SubReddit']
    __Quantity = config['REDDIT']['Quantity']
    __Order = config['REDDIT']['Order']
    __OrderTimeFilter = config['REDDIT']['OrderTimeFilter']