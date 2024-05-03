#Polling version
import os,shutil
import time
import datetime
from telegram.ext import *
from telegram import Bot
from telegram import InputFile
import configparser
import codecs
import tiktokbot
config = configparser.ConfigParser()
config.read(codecs.open("settings.ini","r","utf8"))

Bot = Bot(token="6775246400:AAFhFByRSD_WWRrq6pmtq33y4teYSJIiPIU")
updater = Updater("6775246400:AAFhFByRSD_WWRrq6pmtq33y4teYSJIiPIU", use_context=True)

def start_command(update, context):

    update.message.reply_text("Hello, to learn more about the bot, you can type /help.")

def error(update, context):

    print(context.error)
    Bot.send_message(update.message.chat_id,f'Update caused  "{context.error}" error. Please contact the developer at sandoganali187@gmail.com to report this error.')

def quit():

    updater.stop()
    updater.is_idle= False
def main():
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("url", url))
    dp.add_handler(CommandHandler("setting",settings))
    dp.add_handler(CommandHandler("clearhistory",clearhistory))
    dp.add_handler(CommandHandler("clearzips",clearzips))


    updater.start_polling(5)
    updater.idle()
