
from asyncio.windows_events import NULL
from concurrent.futures import thread
import configparser
from datetime import *
from genericpath import isfile
import os
import pathlib
from pickle import INT
from threading import Thread
import threading
from time import sleep
from tkinter import Variable
from xmlrpc.client import boolean
import telebot
from telebot import types
import os
from os.path import isfile, join
import configparser
import schedule
from ImageTranslator import ImageTranslator
import RedditScraper
from Constants import *
import BotStates
from BotLayoutElements import *
from threading import Thread

config = configparser.ConfigParser()
config.read(TBotConfigFile)
BotToken = config.get('Telegram Bot',"BotToken")
bot = telebot.TeleBot(BotToken)
# Users = [1012947591]
# NewBee = []
Interval = config.get('Telegram Bot',"Interval")
JobStartTime = datetime.now() + timedelta(hours= (int)(Interval[:2]), minutes= (int)(Interval[3:]))
TranslateImage = config.get('Telegram Bot', "translate")
 

@bot.message_handler(commands=["start"])
def startmessage(message):
    # if not os.path.exists(SourceDirectory):
    #     os.makedirs(SourceDirectory)
    # if not os.path.exists(LocalDerictory):
    #     os.makedirs(LocalDerictory)  
    # if message.from_user.id in Users:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(StatusButton, StealButton, SettingsButton)
        bot.send_message(message.from_user.id, "Ready to work!", reply_markup = markup)
        UpdateSchedule()
        ReplyStatus(message)
        Thread(target=schedule_checker).start() 
        bot.polling(none_stop= True, interval= 0)
    # else: 
    #     NewBee.append(message.from_user.id)
    #     bot.send_message(message.from_user.id, "Введи пароль")

# @bot.message_handler(func=lambda message: config.get('Telegram Bot',"State") == BotStates.States.S_START)
# def get_text_messages(message):
#     if message.from_user.id in NewBee:
#         if message.text == PassWord:
#             BotState = BotStates.States.S_FRONTPAGE
#             bot.send_message(message.from_user.id, "Правильный пароль!!!")
#             NewBee.clear
#             Users.append(message.from_user.id)
#             startmessage(message)
#         else:
#             bot.send_message(message.from_user.id, "Неправильный пароль!!!") 
#             bot.send_message(message.from_user.id, "Введи пароль")

@bot.message_handler(func=lambda message: config.get('Telegram Bot',"State") == BotStates.States.S_FRONTPAGE)
def get_text_messages(message):
        if message.text == StatusInputText:
            ReplyStatus(message)
        elif message.text == StealInputText:
            ReplyTest(message)
        elif message.text == SettingsInputText:
            ReplySettings(message)
        
@bot.message_handler(func=lambda message: config.get('Telegram Bot',"State") == BotStates.States.S_STEALNOW)
def get_text_messages(message):
    if message.text == BackInputText:
        ReplyStatus(message)
        return
    elif message.text == '1':
        RedditScraper.ChangeQuantity(1)
        RedditScraper.ChangeOrder('new')
        Job(message.from_user.id)
        RedditScraper.BackupSettings()
    elif message.text == '5':
        RedditScraper.ChangeQuantity(5)
        RedditScraper.ChangeOrder('new')
        Job(message.from_user.id)
        RedditScraper.BackupSettings()
    elif message.text == '10':
        RedditScraper.ChangeQuantity(10)
        RedditScraper.ChangeOrder('new')
        Job(message.from_user.id)
        RedditScraper.BackupSettings()
    elif message.text == '25':
        RedditScraper.ChangeQuantity(25)
        RedditScraper.ChangeOrder('new')
        Job(message.from_user.id)
        RedditScraper.BackupSettings()
    elif message.text == '50':
        RedditScraper.ChangeQuantity(50)
        RedditScraper.ChangeOrder('new')
        Job(message.from_user.id)
        RedditScraper.BackupSettings()
        
    JobStartTime = datetime.now() + timedelta(hours= (int)(Interval[:2]), minutes= (int)(Interval[3:]))

@bot.message_handler(func=lambda message: config.get('Telegram Bot',"State") == BotStates.States.S_SETTINGS)
def get_text_messages(message):
    if message.text == SubredditText:
        ReplyChangeSubreddit(message)
    elif message.text == OrderText:
        ReplyChangeOrder(message)
    elif message.text == TimeFilterText:
        ReplyChangeTimeFilter(message)
    elif message.text == DownloadQuantityText:
        ReplyChangeQuantity(message)
    elif message.text == IntervalText:
        ReplyChangeInterval(message)
    elif message.text == TranslitionText:
        ReplyChangeTranslate(message)
    elif message.text == BackInputText:
        ReplyStatus(message)
        
@bot.message_handler(func=lambda message: config.get('Telegram Bot',"State") == BotStates.States.S_SETSUBREDDIT)
def get_text_messages(message):
    if message.text == BackInputText:
        ReplySettings(message)
    elif (RedditScraper.ChangeSubreddit(message.text)):
        bot.send_message(message.from_user.id, "Subreddit changed!!!")
        ReplySettings(message)
    else:
        bot.send_message(message.from_user.id, "Error! Try again:")
        ReplyChangeSubreddit(message)
        
@bot.message_handler(func=lambda message: config.get('Telegram Bot',"State") == BotStates.States.S_SETORDER)
def get_text_messages(message):
    if message.text == BackInputText:
        ReplySettings(message)
    elif message.text == OrderHotText:
        if RedditScraper.ChangeOrder('hot'):
            bot.send_message(message.from_user.id, "Order changed!!!")
            ReplySettings(message)
        else:
             bot.send_message(message.from_user.id, "Error! Try again:")
             ReplyChangeOrder(message)
    elif message.text == OrderTopText:
        if RedditScraper.ChangeOrder('top'):
            bot.send_message(message.from_user.id, "Order changed!!!")
            ReplySettings(message)
        else:
             bot.send_message(message.from_user.id, "Error! Try again:")
             ReplyChangeOrder(message)
    elif message.text == OrderNewText:
        if RedditScraper.ChangeOrder('new'):
            bot.send_message(message.from_user.id, "Order changed!!!")
            ReplySettings(message)
        else:
            bot.send_message(message.from_user.id, "Error! Try again:")
            ReplyChangeOrder(message)
            
@bot.message_handler(func=lambda message: config.get('Telegram Bot',"State") == BotStates.States.S_SETTIMEFILTER)
def get_text_messages(message):
    if message.text == BackInputText:
        ReplySettings(message)
    elif message.text == 'All':
        if RedditScraper.ChangeOrderTimeFilter('all'):
            bot.send_message(message.from_user.id, "Time order changed!!!")
            ReplySettings(message)
        else:
             bot.send_message(message.from_user.id, "Error! Try again:")
             ReplyChangeTimeFilter(message)
    elif message.text == 'Year':
        if RedditScraper.ChangeOrderTimeFilter('year'):
            bot.send_message(message.from_user.id, "Time order changed!!!")
            ReplySettings(message)
        else:
             bot.send_message(message.from_user.id, "Error! Try again:")
             ReplyChangeTimeFilter(message)
    elif message.text == 'Month':
        if RedditScraper.ChangeOrderTimeFilter('month'):
            bot.send_message(message.from_user.id, "Time order changed!!!")
            ReplySettings(message)
        else:
            bot.send_message(message.from_user.id, "Error! Try again:")
            ReplyChangeTimeFilter(message)
    elif message.text == 'Day':
        if RedditScraper.ChangeOrderTimeFilter('day'):
            bot.send_message(message.from_user.id, "Time order changed!!!")
            ReplyChangeTimeFilter(message)
        else:
            bot.send_message(message.from_user.id, "Error! Try again:")
            ReplyChangeTimeFilter(message)
    elif message.text == 'Hour':
        if RedditScraper.ChangeOrderTimeFilter('hour'):
            bot.send_message(message.from_user.id, "Time order changed!!!")
            ReplySettings(message)
        else:
            bot.send_message(message.from_user.id, "Error! Try again:")
            ReplyChangeTimeFilter(message)
            
@bot.message_handler(func=lambda message: config.get('Telegram Bot',"State") == BotStates.States.S_SETQUANTITY)
def get_text_messages(message):
    if message.text == BackInputText:
        ReplySettings(message)
    elif RedditScraper.ChangeQuantity(message.text):
        bot.send_message(message.from_user.id, "Download quantity changed!!!")
        ReplySettings(message)
    else:
         bot.send_message(message.from_user.id, "Error! Try again:")
         ReplyChangeQuantity(message)

@bot.message_handler(func=lambda message: config.get('Telegram Bot',"State") == BotStates.States.S_SETINTERVAL)
def get_text_messages(message):
    if message.text == BackInputText:
        ReplySettings(message)
    else:
        try:
            TimeNow = datetime.now()
            TimeAfterNewInterval = TimeNow + timedelta(hours= (int)(message.text[:2]), minutes= (int)(message.text[3:]))
            global Interval
            Interval = message.text
            ChangeConfig('interval', message.text)
            UpdateSchedule()
            bot.send_message(message.from_user.id, "Interval changed!!!")
            ReplySettings(message)
        except:
            bot.send_message(message.from_user.id, "Error! Try again:")
            ReplyChangeInterval(message)
        
def ReplyTest(message):
    ChangeConfig('State', BotStates.States.S_STEALNOW)
    OneMemeButton = types.KeyboardButton('1')
    FiveMemeButton = types.KeyboardButton('5')
    TenMemeButton = types.KeyboardButton('10')
    TwentyFiveMemeButton = types.KeyboardButton('25')
    FivetyMemeButton = types.KeyboardButton('50')
    BackButton = types.KeyboardButton(BackInputText)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(OneMemeButton, FiveMemeButton,TenMemeButton,
               TwentyFiveMemeButton, FivetyMemeButton,
               BackButton)
    bot.send_message(message.from_user.id, "How much content to download?", reply_markup = markup)

def ReplyStatus(message):
    ChangeConfig('State', BotStates.States.S_FRONTPAGE)
    TimeNow = datetime.now()
    DeltaTime = JobStartTime - TimeNow
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(StatusButton, StealButton, SettingsButton)
    bot.send_message(message.from_user.id, SubredditText + ": " + (str)(RedditScraper.GetSubreddit()) + "\n"
                                         + "\n"
                                         + OrderText + ": "  + (str)(RedditScraper.GetOrder()) + "\n"
                                         + "\n"
                                         + TimeFilterText + ": " + (str)(RedditScraper.GetOrderTimeFilter()) + "\n"
                                         + "\n"
                                         + DownloadQuantityText + ": " + (str)(RedditScraper.GetQuantity()) + "\n"
                                         + "\n"
                                         + TranslitionText + ": " + (str)(TranslateImage) + "\n"
                                         + "\n"
                                         + IntervalText + ": " + Interval + "\n"
                                         + "\n"
                                         + "Next drop in \U000023F0: \n" + (str)(DeltaTime.seconds//3600) + ':' + (str)(DeltaTime.seconds//60 - DeltaTime.seconds//3600 * 60) + ':' + (str)(DeltaTime.seconds - ((DeltaTime.seconds//3600)*3600) - ((DeltaTime.seconds//60 - DeltaTime.seconds//3600 * 60)*60)), reply_markup = markup)
    
def ReplySettings(message):
    ChangeConfig('State', BotStates.States.S_SETTINGS)
    ChangeSubredditButton = types.KeyboardButton(SubredditText)
    ChangeOrderButton = types.KeyboardButton(OrderText)
    ChangeTimeFilterButton = types.KeyboardButton(TimeFilterText)
    ChangeQuantityButton = types.KeyboardButton(DownloadQuantityText)
    ChangeIntervalButton = types.KeyboardButton(IntervalText)
    ChangeTranslateButton = types.KeyboardButton(TranslitionText)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(ChangeSubredditButton,ChangeOrderButton,ChangeTimeFilterButton,
               ChangeQuantityButton, ChangeIntervalButton, ChangeTranslateButton, BackButton)
    bot.send_message(message.from_user.id, "Change "  + SubredditText + " : " + (str)(RedditScraper.GetSubreddit()) + "\n"
                                         + "\n"
                                         + "Change "  + OrderText + " : " + (str)(RedditScraper.GetOrder()) + "\n"
                                         + "\n"
                                         + "Change "  + TimeFilterText + " : " + (str)(RedditScraper.GetOrderTimeFilter()) + "\n"
                                         + "\n"
                                         + "Change "  + DownloadQuantityText + " : " + (str)(RedditScraper.GetQuantity()) + "\n"
                                         + "\n"
                                         + "Change "  + IntervalText + " : " + (str)(Interval) + "\n"
                                         + "\n"
                                         + "Change "  + TranslitionText + " : " + (str)(TranslateImage), reply_markup = markup)
    
def ReplyChangeSubreddit(message):
    ChangeConfig('State', BotStates.States.S_SETSUBREDDIT)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(BackButton)
    bot.send_message(message.from_user.id, "Write subreddit name (без /r)", reply_markup = markup)

def ReplyChangeOrder(message):
    ChangeConfig('State', BotStates.States.S_SETORDER)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    OrderHotButton = types.KeyboardButton(OrderHotText)
    OrderTopButton = types.KeyboardButton(OrderTopText)
    OrderNewButton = types.KeyboardButton(OrderNewText)
    markup.add(OrderHotButton,OrderTopButton,OrderNewButton,BackButton)
    bot.send_message(message.from_user.id, "Choose order ", reply_markup = markup)
    
def ReplyChangeTimeFilter(message):
    ChangeConfig('State', BotStates.States.S_SETTIMEFILTER)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    TimeFilterAllButton = types.KeyboardButton('All')
    TimeFilterYearButton = types.KeyboardButton('Year')
    TimeFilterMonthButton = types.KeyboardButton('Month')
    TimeFilterDayButton = types.KeyboardButton('Day')
    TimeFilterHourButton = types.KeyboardButton('Hour')
    markup.add(TimeFilterHourButton, TimeFilterDayButton, TimeFilterMonthButton,
               TimeFilterYearButton, TimeFilterAllButton, BackButton)
    bot.send_message(message.from_user.id, "Choose time order", reply_markup = markup)
    
def ReplyChangeQuantity(message): 
    ChangeConfig('State', BotStates.States.S_SETQUANTITY)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(BackButton)
    bot.send_message(message.from_user.id, "Write download qquantity:", reply_markup = markup)
    
def ReplyChangeInterval(message):
    ChangeConfig('State', BotStates.States.S_SETINTERVAL)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(BackButton)
    bot.send_message(message.from_user.id, "Write interval in 24-hour format (HH:MM)", reply_markup = markup)

def ReplyChangeTranslate(message):
    global TranslateImage
    ChangeConfig('translate', "false" if TranslateImage == "true" else "true")
    bot.send_message(message.from_user.id, "Translate option changed!!!")
    TranslateImage = config.get('Telegram Bot', "translate")
    ReplySettings(message)
            
def ChangeConfig(Title, Value):
    config['Telegram Bot'][Title] = Value
    with open(TBotConfigFile, mode = "w") as configfile:
        config.write(configfile)
    config.read(TBotConfigFile)

def ProcessImage(file, SendDirectory, Func, id):
    if (Func != NULL):
        Func(file)
    try:
        bot.send_photo(id, photo=open(SendDirectory + file, 'rb'))
    except:
        bot.send_message(id, "Error with Telegram sending")
        

def Job(id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(WaitButton)
    bot.send_message(id, "Begin download...", reply_markup = markup)
    config.set('Telegram Bot',"State", BotStates.States.S_PROCESSING)
    if (RedditScraper.RedditDownload()):
        bot.send_message(id, "Download complete!")
        try:
            func = NULL
            onlyfiles = [f for f in os.listdir(SourceDirectory) if isfile(join(SourceDirectory, f))]
            SendDirectory = SourceDirectory
            if (TranslateImage == 'true'):
                bot.send_message(id, "Start translating!")
                SendDirectory = LocalDerictory
                func = ImageTranslator.Run
   
            for sourcefileineng in onlyfiles:
                t = Thread(target = ProcessImage, args = (sourcefileineng, SendDirectory, func, id))
                t.run()
        except:
            bot.send_message(id, "Some Error Occured")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(StatusButton, StealButton, SettingsButton)
        bot.send_message(id, "End download...", reply_markup = markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(StatusButton, StealButton, SettingsButton)
        bot.send_message(id, "Error with Reddit library! ", reply_markup = markup) 
    config.set('Telegram Bot',"State", BotStates.States.S_PROCESSING)
    UpdateSchedule()
   
def UpdateSchedule():
    global JobStartTime
    JobStartTime = datetime.now() + timedelta(hours=(int)(Interval[:2]), minutes= (int)(Interval[3:]))
    hr = (str)(JobStartTime.hour)
    if (len(hr) == 1): 
        hr = '0'+ hr
    mnt = (str)(JobStartTime.minute)
    if (len(mnt) == 1): 
        mnt = '0'+ mnt
    schedule.clear()
    schedule.every().day.at(hr + ':' + mnt).do(Job, 1012947591)

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)
        
bot.polling(none_stop= True, interval= 0)
