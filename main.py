#Paid Project - this version of the project is way upgraded from the project described on the github link
#https://github.com/DoganAliSAN/TSB
#DALIS 
import tkinter
import tkinter.filedialog
import customtkinter as ct
import os
import time
import datetime
import threading
import subprocess
ct.set_appearance_mode("System")
ct.set_default_color_theme("blue")
widgets = []
def slider_event(value):
    global values
    values = value
    var.set("Video Count: " + str(int(value)))
def select_path():
    global path
    path = tkinter.filedialog.askdirectory()
    print(path)


def start():
    from tiktokbot import TiktokBot

    if not os.path.exists("videos"):
        os.mkdir("videos")
    if not os.path.exists("oldlinks"):
        os.mkdir("oldlinks")
    if not os.path.exists("txts"):
        os.mkdir("txts")
    tag = entry.get()
    print(tag)
    chat_id = "0100010001101111011001110110000101101110"
    info_label.configure(text=f"Searching for compatible videos.", fg_color="yellow")

    list = TiktokBot.get_like_and_comment_from_tag(values, tag, chat_id)
    if (len(list) == 0):
        info_label.configure(
            text="I couldn't find any video that matches your request :(", fg_color="red")
    else:
        import shutil
        from tiktok_module import downloader
        shutil.rmtree("videos")
        os.mkdir("videos")
        dl = downloader.tiktok_downloader()
        for i in range(len(list)):
            try:
                time.sleep(7)
                dl.musicaldown(url=list[i], output_name=f"videos/{i}.mp4")
            except:
                print("something is wrong with video download")
            parts = list[i].split('@')
            username = parts[1].split("/")[0]
            info_label.configure(
                text=f"The videos are being prepared.", fg_color="yellow")

            TiktokBot.watermark(username, i, tag)

            try:
                os.remove(f"videos/{i}.mp4")
            except:
                with open("error.txt", "a+") as f:
                    message = f"\nCan't delete video files because they do not exist  | {datetime.datetime.now()}\n"
                    f.write(message)
        zip_name = f"{tag}_0"
        zip_dir = path
        zip_path = os.path.join(zip_dir, zip_name)

        if not os.path.exists(zip_dir):
            os.makedirs(zip_dir)

        shutil.make_archive(base_name=zip_path,
                            format='zip', root_dir="videos")
        info_label.configure(
            text=f'Zip "{path}" was saved to the path.', fg_color="green")


def start_thread():
    t = threading.Thread(target=start)
    t.start()


def uygulama():
    for widget in widgets:
        widget.configure(state="normal")
    enable_button.configure(state="disabled")
    telegrammodule.quit()


def telegram():
    global enable_button, telegrammodule
    import telegrammodule
    for widget in widgets:
        widget.configure(state="disabled")

    enable_button = ct.CTkButton(
        master=app, text="Back To App", command=uygulama)
    enable_button.place(relx=0.5, rely=0.1)

    if not os.path.exists("videos"):
        os.mkdir("videos")
    if not os.path.exists("oldlinks"):
        os.mkdir("oldlinks")
    if not os.path.exists("txts"):
        os.mkdir("txts")

    print("Bot Started")
    x = threading.Thread(target=telegrammodule.main)
    x.start()


def telegram_thread():
    t2 = threading.Thread(target=telegram)
    t2.start()


def open_settings_file():
    subprocess.Popen(["notepad.exe","./settings.ini"])


app = ct.CTk()
app.geometry("800x500")
app.title("TSB")

entry = ct.CTkEntry(master=app, placeholder_text="HashTag:")
entry.pack(side="left", anchor="nw", padx=20, pady=20)
widgets.append(entry)

var = tkinter.StringVar()
var.set("Video Count:")


label = ct.CTkLabel(master=app, textvariable=var)
label.place(relx=0.03, rely=0.15)
widgets.append(label)

slider = ct.CTkSlider(master=app, from_=1, to=100, command=slider_event)
slider.pack(side="left", anchor="nw", padx=20, pady=20)
slider.place(relx=0.02, rely=0.2)
widgets.append(slider)

select_path_button = ct.CTkButton(master=app, text="Select Path", command=select_path)
select_path_button.pack(side="left", anchor="nw", padx=20, pady=20)
select_path_button.place(relx=0.02, rely=0.3)
widgets.append(select_path_button)

start_ = ct.CTkButton(master=app, text="Start", command=start_thread)
start_.place(relx=0.02, rely=0.4)
widgets.append(start_)

settings_button = ct.CTkButton(
    master=app, text="Open Settings", command=open_settings_file)
settings_button.place(relx=0.3, rely=0.4)

info_label = ct.CTkLabel(master=app, text="", width=300,
                         height=75, text_color="black")
info_label.pack(fill="x")
info_label.place(relx=0.02, rely=0.5)
widgets.append(info_label)


telegram_ = ct.CTkButton(master=app, text="Telegram", command=telegram_thread)
telegram_.place(relx=0.5, rely=0.03)
widgets.append(telegram_)


app.mainloop()
