import codecs
import platform
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time,datetime
import configparser
def drv():
    global driver
    op = uc.ChromeOptions()
    #op.add_argument("--headless")
    op.add_argument("--mute-audio")
    if platform.system() == "Windows":
        op.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        driver = uc.Chrome(options=op,enable_cdp_events=True)
    elif platform.system() == "Darwin":
        op.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        driver = uc.Chrome(options=op)
    else:
        return None

def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)

def scroll_to_bottom(driver,amount):
    time.sleep(3)
    for i in range(amount):
        driver.execute_script((
            "var scrollingElement = (document.scrollingElement ||"
            " document.body);scrollingElement.scrollTop ="
            " scrollingElement.scrollHeight;"))

class TiktokBot(BaseException):

    def get_like_and_comment_from_tag(ran, tag, chatid):
        drv()
        config = configparser.ConfigParser()
        config.read(codecs.open("./settings.ini","r","utf8"))
        driver.get("https://tiktok.com/tag/"+tag)
        if not int(ran) < 14:
            scroll_to_bottom(driver,3)
        else:pass

        delay = 15
        videourls = []

        oldlink_path = f"oldlinks/old_links-{chatid}.txt"
        old_links = open(oldlink_path, "a+")
        link_count = 0
        i = 1
        failed = 0 
        while link_count < int(ran):
            try:
                element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                    (By.XPATH, f'//*[@id="main-content-challenge"]/div/div[2]/div/div[{i}]/div[1]/div/div/a/div/div[1]/div/span/picture/img')))

                driver.execute_script("arguments[0].click()", element)
                url = driver.current_url
                with open(oldlink_path, "r") as f:
                    cont = f.read()
                    if url in cont:

                        time.sleep(3)
                        i += 1
                    else:
                        likes = convert_str_to_number(driver.find_element(
                            By.XPATH, '//*[@id="app"]/div[2]/div[4]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[1]/div[1]/button[1]/strong').text)
                            

                        print("likes",likes)
                        comments = convert_str_to_number(driver.find_element(
                            By.XPATH, '//*[@id="app"]/div[2]/div[4]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[1]/div[1]/button[2]/strong').text)
                        print("comments",comments)

                        if (likes > int(config["TIKTOKVIDEOS"]["like"]) and comments > int(config["TIKTOKVIDEOS"]["comment"])):
                            videourls.append(url)
                            old_links.write(url+"\n")

                            link_count += 1
                            i += 1
                            failed = 0 
                        else:

                            i += 1
                            failed += 1 
                            if failed == 15:
                                break
                       

            except NoSuchElementException:
                with open("error.txt","a+") as f :
                    f.write(f"NoSuchElementException {datetime.datetime.now()}")
                time.sleep(10)
                driver.get("https://tiktok.com/tag/"+tag)
                scroll_to_bottom(driver,3)
                i += 1

            except TimeoutException:
                with open("error.txt","a+") as f :
                    f.write(f"TimeOutException {datetime.datetime.now()}")
                time.sleep(10)
                driver.get("https://tiktok.com/tag/"+tag)
                scroll_to_bottom(driver,3)
                i += 1

            except Exception as e:
                with open("error.txt","a+") as f :
                    f.write(f"{str(e)} {datetime.datetime.now()}")
                time.sleep(10)
                driver.get("https://tiktok.com/tag/"+tag)
                scroll_to_bottom(driver,3)
                i += 1

        old_links.close()
        
        return videourls

    def watermark(otheraccount,id,tag):
        import subprocess
        import codecs
        config = configparser.ConfigParser()
        config.read_file(codecs.open("./settings.ini","r","utf8"))

        # Input video file
        input_file = f"videos/{id}.mp4"

        # Output video file
        output_file = f"videos/{id}_{tag}.mp4"

        # Texts
        if config is not None:
            texts = [{'text':str(otheraccount), 'x':'W-200', 'y':'120'},
                    {'text':str(config["WATERMARK"]["watermark"]), 'x':'120', 'y':'H-200'}]

        texts = [{'text':str(otheraccount), 'x':'W-200', 'y':'120'},
                {'text':str(config["WATERMARK"]["watermark"]), 'x':'120', 'y':'H-200'}]

        # Font
        font = 'fonts/arial.ttf'

        # Font size
        font_size = '30'

        # Font color
        font_color = 'white'


        # Drawtexts
        drawtexts = ','.join([f'drawtext="fontfile={font}:text={t["text"]}:x={t["x"]}:y={t["y"]}:fontsize={font_size}:fontcolor={font_color}"' for t in texts])

        # Run command
        subprocess.run(f'ffmpeg -i {input_file} -vf {drawtexts} -y {output_file}', shell=True)
