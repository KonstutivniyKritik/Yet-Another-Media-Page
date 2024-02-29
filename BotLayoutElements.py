from telebot import types


StatusInputText = "\U0001F4CA Статус"
StealInputText = '\U0001F640 Воровство СЕЙЧАС!!!'
SettingsInputText = '\U00002699 Настройки'
BackInputText = '\U0000274C Назад'
StatusButton = types.KeyboardButton(StatusInputText)
StealButton = types.KeyboardButton(StealInputText)
SettingsButton = types.KeyboardButton(SettingsInputText)
BackButton = types.KeyboardButton(BackInputText)s