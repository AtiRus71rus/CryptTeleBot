#!/usr/bin/env python
# coding: utf-8

# In[2]:


import telebot
from telebot import types
import tkinter as tk
from tkinter.filedialog import askopenfilename


# In[ ]:


bot = telebot.TeleBot('5637246216:AAHPUR1ZiM0dsx3QLd7yxcbMnZvPH0SFRgI')
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Выбрать файл")
    markup.add(btn1)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я - лог-бот для биржевой системы! Выберите ini-файл для обозначения настроек работы бота:".format(message.from_user), reply_markup=markup)
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Поздороваться"):
        bot.send_message(message.chat.id, text="Привет!)")
    elif(message.text == "Выбрать файл"):
        filename = askopenfilename()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton("Изменить файл")
        markup.add(btn2)
        bot.send_message(message.chat.id, text="Вы можете нажать клавишу Изменить файл, чтобы изменить текущие настройки", reply_markup=markup)
@bot.message_handler(commands=['searchfile'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Выберите файл")
    markup.add(item1)
    bot.send_message(message.chat.id,'Выберите файл',reply_markup=markup)
bot.infinity_polling()


# In[ ]:





# In[ ]:




