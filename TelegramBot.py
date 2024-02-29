
import configparser
from datetime import *
from genericpath import isfile
import os
import pathlib
from threading import Thread
from time import sleep
from tkinter import Variable
import telebot
from telebot import types
import os
from os.path import isfile, join
import configparser
import schedule
import RedditScraper
from Constants import *
import BotStates
from BotLayoutElements import *

config = configparser.ConfigParser()
config.read(TBotConfigFile)
BotToken = config.get('Telegram Bot',"BotToken")
bot = telebot.TeleBot(BotToken)
# Users = [1012947591]
# NewBee = []
Interval = config.get('Telegram Bot',"Interval")
JobStartTime = datetime.now() + timedelta(hours= (int)(Interval[:2]), minutes= (int)(Interval[3:]))

 

@bot.message_handler(commands=["start"])
def startmessage(message):
    # if not os.path.exists(SourceDirectory):
    #     os.makedirs(SourceDirectory)
    # if not os.path.exists(LocalDerictory):
    #     os.makedirs(LocalDerictory)  
    # if message.from_user.id in Users:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(StatusButton, StealButton, SettingsButton)
        bot.send_message(message.from_user.id, "Я родился и готов воровать!!!", reply_markup = markup)
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
    if message.text == '1':
        ReplyChangeSubreddit(message)
    elif message.text == '2':
        ReplyChangeOrder(message)
    elif message.text == '3':
        ReplyChangeTimeFilter(message)
    elif message.text == '4':
        ReplyChangeQuantity(message)
    elif message.text == '5':
        ReplyChangeInterval(message)
    elif message.text == BackInputText:
        ReplyStatus(message)
        
@bot.message_handler(func=lambda message: config.get('Telegram Bot',"State") == BotStates.States.S_SETSUBREDDIT)
def get_text_messages(message):
    if message.text == BackInputText:
        ReplySettings(message)
    elif (RedditScraper.ChangeSubreddit(message.text)):
        bot.send_message(message.from_user.id, "Сабреддит успешно изменен!!!")
        ReplySettings(message)
    else:
        bot.send_message(message.from_user.id, "Ошибка! Попробуйте снова:")
        ReplyChangeSubreddit(message)
        
@bot.message_handler(func=lambda message: config.get('Telegram Bot',"State") == BotStates.States.S_SETORDER)
def get_text_messages(message):
    if message.text == BackInputText:
        ReplySettings(message)
    elif message.text == '\U0001F525 Горячее':
        if RedditScraper.ChangeOrder('hot'):
            bot.send_message(message.from_user.id, "Порядок успешно изменен!!!")
            ReplySettings(message)
        else:
             bot.send_message(message.from_user.id, "Ошибка! Попробуйте снова:")
             ReplyChangeOrder(message)
    elif message.text == '\U0001F4A5 Лучшее':
        if RedditScraper.ChangeOrder('top'):
            bot.send_message(message.from_user.id, "Порядок успешно изменен!!!")
            ReplySettings(message)
        else:
             bot.send_message(message.from_user.id, "Ошибка! Попробуйте снова:")
             ReplyChangeOrder(message)
    elif message.text == '\U00002728 Новое':
        if RedditScraper.ChangeOrder('new'):
            bot.send_message(message.from_user.id, "Порядок успешно изменен!!!")
            ReplySettings(message)
        else:
            bot.send_message(message.from_user.id, "Ошибка! Попробуйте снова:")
            ReplyChangeOrder(message)
            
@bot.message_handler(func=lambda message: config.get('Telegram Bot',"State") == BotStates.States.S_SETTIMEFILTER)
def get_text_messages(message):
    if message.text == BackInputText:
        ReplySettings(message)
    elif message.text == 'Все время':
        if RedditScraper.ChangeOrderTimeFilter('all'):
            bot.send_message(message.from_user.id, "Время выборки успешно изменено!!!")
            ReplySettings(message)
        else:
             bot.send_message(message.from_user.id, "Ошибка! Попробуйте снова:")
             ReplyChangeTimeFilter(message)
    elif message.text == 'Год':
        if RedditScraper.ChangeOrderTimeFilter('year'):
            bot.send_message(message.from_user.id, "Время выборки успешно изменено!!!")
            ReplySettings(message)
        else:
             bot.send_message(message.from_user.id, "Ошибка! Попробуйте снова:")
             ReplyChangeTimeFilter(message)
    elif message.text == 'Месяц':
        if RedditScraper.ChangeOrderTimeFilter('month'):
            bot.send_message(message.from_user.id, "Время выборки успешно изменено!!!")
            ReplySettings(message)
        else:
            bot.send_message(message.from_user.id, "Ошибка! Попробуйте снова:")
            ReplyChangeTimeFilter(message)
    elif message.text == 'День':
        if RedditScraper.ChangeOrderTimeFilter('day'):
            bot.send_message(message.from_user.id, "Время выборки успешно изменено!!!")
            ReplyChangeTimeFilter(message)
        else:
            bot.send_message(message.from_user.id, "Ошибка! Попробуйте снова:")
            ReplyChangeTimeFilter(message)
    elif message.text == 'Час':
        if RedditScraper.ChangeOrderTimeFilter('hour'):
            bot.send_message(message.from_user.id, "Время выборки успешно изменено!!!")
            ReplySettings(message)
        else:
            bot.send_message(message.from_user.id, "Ошибка! Попробуйте снова:")
            ReplyChangeTimeFilter(message)
            
@bot.message_handler(func=lambda message: config.get('Telegram Bot',"State") == BotStates.States.S_SETQUANTITY)
def get_text_messages(message):
    if message.text == BackInputText:
        ReplySettings(message)
    elif RedditScraper.ChangeQuantity(message.text):
        bot.send_message(message.from_user.id, "Количество мемов успешно изменено!!!")
        ReplySettings(message)
    else:
         bot.send_message(message.from_user.id, "Ошибка! Попробуйте снова:")
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
            bot.send_message(message.from_user.id, "Интервал Успешно изменен!!!")
            ReplySettings(message)
        except:
            bot.send_message(message.from_user.id, "Ошибка! Попробуйте снова:")
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
    bot.send_message(message.from_user.id, "Сколько мемов надо?", reply_markup = markup)

def ReplyStatus(message):
    ChangeConfig('State', BotStates.States.S_FRONTPAGE)
    TimeNow = datetime.now()
    DeltaTime = JobStartTime - TimeNow
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(StatusButton, StealButton, SettingsButton)
    bot.send_message(message.from_user.id, "Сабреддит: " + (str)(RedditScraper.GetSubreddit()) + "\n"
                                         + "\n"
                                         + "Порядок: " + (str)(RedditScraper.GetOrder()) + "\n"
                                         + "\n"
                                         + "Временной фильтр: " + (str)(RedditScraper.GetOrderTimeFilter()) + "\n"
                                         + "\n"
                                         + "Количество мемов: " + (str)(RedditScraper.GetQuantity()) + "\n"
                                         + "\n"
                                         + "Интервал воровства \U000023F3: " + Interval + "\n"
                                         + "\n"
                                         + "Следующее воровство через \U000023F0: \n" + (str)(DeltaTime.seconds//3600) + ':' + (str)(DeltaTime.seconds//60 - DeltaTime.seconds//3600 * 60) + ':' + (str)(DeltaTime.seconds - ((DeltaTime.seconds//3600)*3600) - ((DeltaTime.seconds//60 - DeltaTime.seconds//3600 * 60)*60)), reply_markup = markup)
    
def ReplySettings(message):
    ChangeConfig('State', BotStates.States.S_SETTINGS)
    ChangeSubredditButton = types.KeyboardButton('1')
    ChangeOrderButton = types.KeyboardButton('2')
    ChangeTimeFilterButton = types.KeyboardButton('3')
    ChangeQuantityButton = types.KeyboardButton('4')
    ChangeIntervalButton = types.KeyboardButton('5')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(ChangeSubredditButton,ChangeOrderButton,ChangeTimeFilterButton,
               ChangeQuantityButton, ChangeIntervalButton, BackButton)
    bot.send_message(message.from_user.id, "Изменить сабреддит (1): " + (str)(RedditScraper.GetSubreddit()) + "\n"
                                         + "\n"
                                         + "Изменить порядок (2): " + (str)(RedditScraper.GetOrder()) + "\n"
                                         + "\n"
                                         + "Изменить временной фильтр (3): " + (str)(RedditScraper.GetOrderTimeFilter()) + "\n"
                                         + "\n"
                                         + "Изменить количество мемов (4): " + (str)(RedditScraper.GetQuantity()) + "\n"
                                         + "\n"
                                         + "Изменить интервал воровства (5) \n" + (str)(Interval), reply_markup = markup)
    
def ReplyChangeSubreddit(message):
    ChangeConfig('State', BotStates.States.S_SETSUBREDDIT)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(BackButton)
    bot.send_message(message.from_user.id, "Введите название сабреддита (без /r)", reply_markup = markup)

def ReplyChangeOrder(message):
    ChangeConfig('State', BotStates.States.S_SETORDER)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    OrderHotButton = types.KeyboardButton('\U0001F525 Горячее')
    OrderTopButton = types.KeyboardButton('\U0001F4A5 Лучшее')
    OrderNewButton = types.KeyboardButton('\U00002728 Новое')
    markup.add(OrderHotButton,OrderTopButton,OrderNewButton,BackButton)
    bot.send_message(message.from_user.id, "Выберите порядок выборки", reply_markup = markup)
    
def ReplyChangeTimeFilter(message):
    ChangeConfig('State', BotStates.States.S_SETTIMEFILTER)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    TimeFilterAllButton = types.KeyboardButton('Все время')
    TimeFilterYearButton = types.KeyboardButton('Год')
    TimeFilterMonthButton = types.KeyboardButton('Месяц')
    TimeFilterDayButton = types.KeyboardButton('День')
    TimeFilterHourButton = types.KeyboardButton('Час')
    markup.add(TimeFilterHourButton, TimeFilterDayButton, TimeFilterMonthButton,
               TimeFilterYearButton, TimeFilterAllButton, BackButton)
    bot.send_message(message.from_user.id, "Выберите временной отрезок выборки", reply_markup = markup)
    
def ReplyChangeQuantity(message): 
    ChangeConfig('State', BotStates.States.S_SETQUANTITY)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(BackButton)
    bot.send_message(message.from_user.id, "Введите количество мемов:", reply_markup = markup)
    
def ReplyChangeInterval(message):
    ChangeConfig('State', BotStates.States.S_SETINTERVAL)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(BackButton)
    bot.send_message(message.from_user.id, "Введите время в 24-часовом формате (ЧЧ:ММ)", reply_markup = markup)

def ChangeConfig(Title, Value):
    config['Telegram Bot'][Title] = Value
    with open(TBotConfigFile) as configfile:
        config.write(configfile)
    config.read(TBotConfigFile)

def Job(id):
    bot.send_message(id, "Начинаю воровать...", )
    config.set('Telegram Bot',"State", BotStates.States.S_FRONTPAGE)
    if (RedditScraper.RedditDownload()):
        onlyfiles = [f for f in os.listdir(SourceDirectory) if isfile(join(SourceDirectory, f))]
        for sourcefileineng in onlyfiles:
            try:
                bot.send_photo(id, photo=open(SourceDirectory + sourcefileineng, 'rb'))
            except:
                bot.send_message(id, "Не удалось отправить фото", reply_markup = markup)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(StatusButton, StealButton, SettingsButton)
        bot.send_message(id, "Закончил воровать...", reply_markup = markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(StatusButton, StealButton, SettingsButton)
        bot.send_message(id, "Ошибка в части Реддита! ", reply_markup = markup) 
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
