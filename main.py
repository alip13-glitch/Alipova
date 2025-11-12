import telebot
from config import API_KEY

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, text = "Hello World")

@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.chat.id, text = "Представьте себе виртуального помощника, который всегда на связи. Этот бот — ваш надежный спутник в мире информации.")

@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.chat.id, text = "\n start - запуск бота. \nabout - описание бота. \nhelp - выводит список команд.")

bot.polling()