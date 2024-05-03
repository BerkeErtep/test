#webhook version
import requests
from flask import Flask, Response, request
import Constants
from tiktokbot import TiktokBot
import os
token = Constants.API_KEY
app = Flask(__name__)


def send_message(chat_id, text='default'):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=payload)
    return r


def send_file(chat_id, path):
    url = f"https://api.telegram.org/bot{token}/sendDocument?chat_id={chat_id}"
    files = {'document': open(path, "rb")}
    r = requests.post(url, files=files)


def parse_message(message):
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    if txt[0] == '/':
        symbol = txt[1:]
    else:
        symbol = ''
    return chat_id, symbol


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, symbol = parse_message(msg)
        split = symbol.split(" ")
        if not symbol:
            send_message(chat_id, 'Wrong Data')
            return Response('Ok', status=200)
        elif symbol.lower() == "start":
            send_message(
                chat_id, "Hi, you can learn more about this bot by typing /help")
        elif split[0].lower() == "url":
            send_message(chat_id, text="I'm starting to fetch data right now")
            if len(split) == 3:
                ran = split[1]
                tag = split[2]

                try:
                    file = open(f"url-{tag}.txt", "w")
                    driver = TiktokBot.driver

                    list = TiktokBot.get_like_and_comment_from_tag(
                        driver, ran, tag, chat_id)
                    if (len(list) == 0):
                        send_message(
                            chat_id, "I couldn't find any suitable videos! :(")
                    else:
                        for i in range(len(list)):
                            file.write(list[i] + "\n")
                        file.close()
                        send_file(chat_id, file.name)
                        try:
                            os.remove(f"url-{tag}.txt")
                        except:
                            with open("error.txt", "a+") as e:
                                e.write("No such file or directory\n")
                finally:
                    file.close()

                    try:
                        os.remove(f"url-{tag}.txt")
                    except:
                        with open("error.txt", "a+") as e:
                            e.write("No suc file or directory\n")

            else:
                send_message(
                    chat_id, text="Please make sure you wrote command correctly!")
        elif symbol.lower() == "help":
            message = """
            Use /url command to scrape data from TikTok. Url command searches for matches on TikTok. Simply use  “/url 1 trend” this will get you 1 video from trend tag.

Use /setting command to set like and comment numbers. Setting command can take two different parameters likes and comments please make sure you write the setting option correctly. Simply use “/setting likes 5000” 
            """
            send_message(chat_id, text=message)
        elif symbol.lower() == "setting":
            valid = ['likes', 'comments']
            sp1 = split[1]
            sp2 = split[2]
            if split == 3 and str(sp1).isalpha() and str(sp2).isnumeric() and sp1 in valid:
                f = open("settings.py", "r")
                newstring = """"""
                for b in f:
                    if sp1 in b:
                        newstring += f"{sp1} = {sp2}\n"
                    else:
                        newstring += b
                f.close()

                b = open("settings.py", "w")
                b.write(newstring)
                b.close()
                send_message(chat_id, "I changed the settings for you! :) ")
            elif sp1 not in valid:
                send_message(
                    chat_id, f"{sp1} is not valid you can only use [likes, comments]")

            else:
                send_message(
                    chat_id, "Please specify which setting you will change in correct form! example: '/setting likes 300000'")

        return Response('Ok', status=200)
    else:
        return "<h1> Hello </h1>"


def main():

    app.run()

