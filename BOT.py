import datetime
import os
import re
import time
from bs4 import BeautifulSoup
import instaloader
import psutil
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import yt_dlp
from PIL import Image

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3")
options.add_argument("start-maximized")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--lang=en-US')
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
username = os.getlogin().replace("_", " ")
user_data_dir = "C:\\Users\\" + username + "\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\"
options.add_argument("user-data-dir=" + user_data_dir)
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)

# create a class that contains title, description, tags, filename, video_url, and thumbnail
class Video:
    def __init__(self, title, description, filename, video_url, thumbnail):
        self.title = title
        self.description = description
        self.filename = filename
        self.video_url = video_url
        self.thumbnail = thumbnail

    def __str__(self):
        return f"Title: {self.title}\nDescription: {self.description}\nFilename: {self.filename}\nVideo URL: {self.video_url}\nThumbnail: {self.thumbnail}"

    def __repr__(self):
        return f"Title: {self.title}\nDescription: {self.description}\nFilename: {self.filename}\nVideo URL: {self.video_url}\nThumbnail: {self.thumbnail}"
class bot:
    def __init__(self):
        
        self.scraped_insta_file = "Never-Delete-This-Folder/InstaFiles/scrapped_insta_urls.txt"
        self.download_insta_file = "Never-Delete-This-Folder/InstaFiles/downloaded_insta_videos.txt"
        self.insta_accounts_file = "Never-Delete-This-Folder/InstaFiles/insta_accounts.txt"

        self.scraped_YT_file = "Never-Delete-This-Folder/YTFiles/scrapped_yt_urls.txt"
        self.download_YT_file = "Never-Delete-This-Folder/YTFiles/downloaded_yt_videos.txt"
        self.yt_url_file = "Never-Delete-This-Folder/YTFiles/yt_urls.txt"


        self.upload_file = "Never-Delete-This-Folder/upload_videos_info.txt"

        self.scrapped_insta_urls = set()
        self.downloaded_insta_urls = set()
        self.insta_accounts = set()

        self.scrapped_yt_urls = set()
        self.downloaded_yt_urls = set()
        self.yt_urls = set()

        self.video_list = set()
        self.yt_urls = set()

        self.loader = instaloader.Instaloader()

        self.is_insta_monitoring_complete = False

        if not os.path.exists("Never-Delete-This-Folder/InstaFiles"):
            os.makedirs("Never-Delete-This-Folder/InstaFiles")

        if not os.path.exists("Never-Delete-This-Folder/YTFiles"):
            os.makedirs("Never-Delete-This-Folder/YTFiles")

        # if the scraped_insta_file does not exist, create it
        if not os.path.exists(self.scraped_insta_file):
            with open(self.scraped_insta_file, "w") as f:
                f.write("")
                
        # if the scraped_insta_file does not exist, create it
        if not os.path.exists(self.scraped_YT_file):
            with open(self.scraped_YT_file, "w") as f:
                f.write("")
        
        # used to store the urls of the videos that have been scraped(very important file)
        with open(self.scraped_insta_file, "r") as f:
            self.scrapped_insta_urls = set(f.read().splitlines())

        with open(self.scraped_YT_file, "r") as f:
            self.scrapped_yt_urls = set(f.read().splitlines())

        #  used to check in case the bot crashes, video is scraped but not downloaded
        if os.path.exists(self.download_insta_file):
            with open(self.download_insta_file, "r") as f:
                self.downloaded_insta_urls = set(f.read().splitlines())

        if os.path.exists(self.download_YT_file):
            with open(self.download_YT_file, "r") as f:
                self.downloaded_yt_urls = set(f.read().splitlines())
        # print("3")

            #create an empty set of video class objects
        
            #  used to populate download table in gui
            
        if os.path.exists(self.upload_file):
            with open(self.upload_file, 'r', encoding='utf-8') as file:
                self.video_list = {Video(*line.strip().split(";;;;;")) for line in file}
                # print("2")

        
            # if the self.insta_accounts_file does not exist, create it
        if not os.path.exists(self.insta_accounts_file):
            with open(self.insta_accounts_file, "w") as f:
                f.write("")
                # print("abc")
        else:
            with open(self.insta_accounts_file, "r") as f:
                self.insta_accounts = set(f.read().splitlines())
                # print("xyz")

        # print("1")

        #YOutube 
        if not os.path.exists(self.yt_url_file):
            with open(self.yt_url_file, "w") as f:
                f.write("")
        else:
            with open(self.yt_url_file, "r") as f:
                self.yt_urls = set(f.read().splitlines())

    def scrape_insta(self, url, isNewPage):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'brave.exe':
                try:
                    proc.kill()
                    print("Process terminated successfully.")
                except psutil.NoSuchProcess:
                    print("Process does not exist.")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        UniqueUrls = set()
        try:
            print('Starting the browser...')
            driver.get(f"https://www.instagram.com/{url}/")
            time.sleep(5)
            Insta_Urls = set()
            anchors = driver.find_elements(By.TAG_NAME, "a")
            for anchor in anchors:
                try:
                    svg = anchor.find_element(By.TAG_NAME, "svg")
                    if svg.get_attribute("aria-label") == "Clip" or svg.get_attribute("aria-label") == "Video":
                        href = anchor.get_attribute("href")
                        Insta_Urls.add(href)
                        print(href)
                except NoSuchElementException:
                    continue

            print(len(Insta_Urls))
            UniqueUrls = Insta_Urls.difference(self.scrapped_insta_urls)
            # Add the new Insta_Urls to the set
            Insta_Urls = Insta_Urls.union(self.scrapped_insta_urls)
            print("Found", len(Insta_Urls), "videos")
            with open("Never-Delete-This-Folder/InstaFiles/scrapped_insta_urls.txt", "w") as f:
                for link in Insta_Urls:
                    f.write(link +"\n")
            print(UniqueUrls)
            self.is_insta_monitoring_complete = True
            
            if not isNewPage:
                driver.quit()
                self.download_videos(UniqueUrls)
        except Exception as e:
            print(e)
        finally:
            driver.quit()

    def scrape_yt(self,url, isNewPage):

        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'brave.exe':
                try:
                    proc.kill()
                    print("Process terminated successfully.")
                except psutil.NoSuchProcess:
                    print("Process does not exist.")


        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        UniqueUrls = set()
        try:
            print('Starting the browser...')
            driver.get(f"{url}/videos")
            time.sleep(5)

            anchors = set()
            anchors = driver.find_elements(By.TAG_NAME, "a")
            anchors = {a.get_attribute('href') for a in anchors}
            anchors = {a for a in anchors if str(a).__contains__("/watch?")}

                    
            UniqueUrls = anchors.difference(self.scrapped_yt_urls)
            # Add the new Insta_Urls to the set
            anchors = anchors.union(self.scrapped_yt_urls)

            with open(self.scraped_YT_file, "w") as f:
                for link in anchors:
                    f.write(link +"\n")


            print("Found", len(UniqueUrls), "videos")
            print(UniqueUrls)


        except Exception as e:
            print(e)
        finally:
            driver.quit()
        if(isNewPage == False):
            self.Youtube_Downloader(UniqueUrls)

    def remove_special_characters(self, filename):
        # Define the pattern for allowed characters (alphanumeric, underscore, and hyphen)
        pattern = r'[^a-zA-Z0-9_ .-]'
        # Remove special characters from the filename
        cleaned_filename = re.sub(pattern, '', filename)
        return cleaned_filename

    def Youtube_Downloader(self, video_urls):
        try:
            for video_url in video_urls:
                ydl_opts = {
                    'format': 'best', 
                    'writethumbnail': True,
                    'writeinfojson': True,  
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=False)
                    video_title = info_dict['title']
                    filename = self.remove_special_characters(video_title) 
                    ydl_opts['outtmpl'] = f"Videos/{filename}.%(ext)s"
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                    
                # Convert thumbnail from WebP to JPG
                thumbnail_path = f"Videos/{filename}.webp"
                jpg_thumbnail_path = f"Videos/{filename}.jpg"
                if os.path.exists(thumbnail_path):
                    Image.open(thumbnail_path).convert("RGB").save(jpg_thumbnail_path, "JPEG")
                    os.remove(thumbnail_path)

                # Delete the JSON file
                json_file_path = f"Videos/{filename}.info.json"
                if os.path.exists(json_file_path):
                    os.remove(json_file_path)
             
                soup = BeautifulSoup(requests.get(video_url).content, 'html.parser')
                pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
                description = pattern.findall(str(soup))[0].replace('\\n','\n')
                description = self.remove_emojis(description)

                # add the url to the downloaded_yt_urls file
                with open(self.download_YT_file, "a") as f:
                    f.write(video_url + "\n")
                # create a video object and add it to the video_list
                video = Video(filename, description.replace("\n"," "), f"{filename}.mp4", video_url, f"{filename}.jpg")
                self.video_list.add(video)
                desc = (video.description).replace("\n","")
                # add the video object to the upload_videos_info.txt file
                with open(self.upload_file, 'a', encoding='utf-8') as file:  # Specify the encoding as 'utf-8'
                    file.write(f"{video.title};;;;;{self.remove_emojis(desc)};;;;;{video.filename};;;;;{video.video_url};;;;;{video.thumbnail}\n")
                print("Completed download function")
        except Exception as e:
            print("An error occurred during the download:", str(e))
            
    def delete_files_with_specific_extensions(self,directory, extensions):
        for root, dirs, files in os.walk(directory):
            for file in files:
                filename, file_extension = os.path.splitext(file)
                if file_extension.lower() in extensions:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")

    
    def download_videos(self,Insta_Urls):
        for url in Insta_Urls:
            try:
                post = instaloader.Post.from_shortcode(self.loader.context, url.split("/")[-2])
                directory_path="Videos"
                Description_Tags=post.caption # Ye le gando 
                # Find the index of the first '#' character
                first_hash_index = Description_Tags.find('#')

                # Extract the description and tags
                description = Description_Tags[:first_hash_index].strip().replace(",", " ").replace("\n"," ")
                description = self.remove_emojis(description)
                tags = Description_Tags[first_hash_index :].strip().replace(",", " ")

                Title = str(datetime.datetime.now()).replace(":","_")

                self.loader.filename_pattern = Title
                self.loader.download_post(post, target=directory_path)
                print("Video downloaded successfully.")
                # Specify the extensions of files to delete
                extensions_to_delete = ['.xz','.txt']
                # Call the function to delete the files
                self.delete_files_with_specific_extensions(directory_path, extensions_to_delete)
                # add the url to the downloaded_insta_urls file
                with open(self.download_insta_file, "a") as f:
                    f.write(url + "\n")
                # create a video object and add it to the insta_video_list
                video = Video(Title, description + " " +tags, f"{Title}.mp4", url, f"{Title}.jpg")
                self.video_list.add(video)
                desc = (video.description).replace("\n","")
                # add the video object to the upload_videos_info.txt file
                with open(self.upload_file, 'a', encoding='utf-8') as file:  # Specify the encoding as 'utf-8'
                    file.write(f"{video.title};;;;;{self.remove_emojis(desc)};;;;;{video.filename};;;;;{video.video_url};;;;;{video.thumbnail}\n")

            except Exception as e:
                # gui pe error message show krna hai
                print("An error occurred during the download:", str(e))
                continue
            
        # upload_videos_to_youtoob(Insta_Urls)


    def upload_videos_to_youtoob(self, video):
        lulli_size_video = False
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'brave.exe':
                try:
                    proc.kill()
                    print("Process terminated successfully.")
                except psutil.NoSuchProcess:
                    print("Process does not exist.")
        # print("Youtube uploader ma gaya ha")
        bot = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        time.sleep(5)

        bot.get("https://studio.youtube.com")
        time.sleep(3)
        upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
        upload_button.click()
        time.sleep(1)

        file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
        simp_path = f'Videos/{video.filename}'
        abs_path = os.path.abspath(simp_path)
        file_input.send_keys(abs_path)
        time.sleep(7)

        title_input = bot.find_element(By.XPATH, '//*[@aria-label="Add a title that describes your video (type @ to mention a channel)"]')
        title_input.clear()
        print(video.title)
        has_date = re.search(r'\d{4}-\d{2}-\d{2}', video.title) is not None

        if has_date:
            new_title="Unveiling the Extraordinary: Chronicles of Curiosity on a Journey Beyond Boundaries"
            title_input.send_keys(new_title)
            time.sleep(1)
        else:
            title_input.send_keys(video.title)
            time.sleep(1)
        
        description_input = bot.find_element(By.XPATH, '//*[@aria-label="Tell viewers about your video (type @ to mention a channel)"]')
        description_input.clear()
        description_input.send_keys(self.remove_emojis(video.description))
        time.sleep(1)

        try:
            thumbnail_button = bot.find_element(By.XPATH, '//button[@class="remove-default-style style-scope ytcp-still-cell"]')
            thumbnail_button.click()
            time.sleep(1)
                # Find the thumbnail file input element
            thumbnail_file_input = bot.find_element(By.XPATH, '//input[@type="file"]')
            thumbnail_path = f'Videos/{video.thumbnail}'
            absolute_path = os.path.abspath(thumbnail_path)
            thumbnail_file_input.send_keys(absolute_path)
            time.sleep(1)
        except:
            lulli_size_video = True
            print("Thumbnail can't be changed for short videos")  
        finally:
            next_button = bot.find_element(By.XPATH, '//*[@id="next-button"]')
            for i in range(3):
                next_button.click()
                time.sleep(1)
            done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
            done_button.click()
            try:
                    # remove the uploaded video's object from video_list set and delete files from Videos Folder
                    self.video_list.remove(video)
                    os.remove(f"Videos/{video.filename}")
                    os.remove(f"Videos/{video.thumbnail}")
                    # write the remaining videos to the upload_videos_info.txt file
                    with open(self.upload_file, 'w', encoding='utf-8') as file:  # Specify the encoding as 'utf-8'
                        for video in self.video_list:
                            file.write(f"{video.title};;;;;{video.description};;;;;{video.filename};;;;;{video.video_url};;;;;{video.thumbnail}\n")
                    if lulli_size_video == False:
                        print("large video")
                        WebDriverWait(bot, 600).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Your private video is still processing standard definition (SD).")]')))
                    time.sleep(60)
                    # close_button = bot.find_element(By.XPATH, '//button[@aria-label="Close"]')
                    # close_button.click()
                    bot.quit()
            except Exception as e:
                print("gar bar: ", str(e))
                pass
            bot.quit()

    # monitoring waly button pe click krne se ye function call hoga
    def start_insta_monitoring(self, isNewPage):

        existing_accounts = set()  # Set to store existing accounts from the previous monitoring session

            # Read the existing accounts from the self.insta_accounts_file
        if os.path.exists(self.insta_accounts_file):
            with open(self.insta_accounts_file, "r") as f:
                existing_accounts = {line.strip() for line in f.read().splitlines()}

        if len(existing_accounts) > 0:
            new_accounts =  existing_accounts  - self.insta_accounts # Set of new accounts to be scraped

            print(f"new accounts: {new_accounts} ")
            # Scrape videos for new accounts with True and for existing accounts with False
            if isNewPage == True:
                for url in new_accounts:
                    self.scrape_insta(url, url in new_accounts)
            else:
                for url in existing_accounts:
                    self.scrape_insta(url, url in new_accounts)

            self.insta_accounts = existing_accounts.copy()

    def start_yt_monitoring(self, isNewPage):

        existing_accounts = set()  # Set to store existing accounts from the previous monitoring session

            # Read the existing accounts from the self.insta_accounts_file
        if os.path.exists(self.yt_url_file):
            with open(self.yt_url_file, "r") as f:
                existing_accounts = {line.strip() for line in f.read().splitlines()}

        if len(existing_accounts) > 0:
            new_accounts =  existing_accounts  - self.yt_urls # Set of new accounts to be scraped

            print(f"new accounts: {new_accounts} ")
            # Scrape videos for new accounts with True and for existing accounts with False
            if isNewPage == True:
                for url in new_accounts:
                    self.scrape_yt(url, url in new_accounts)
            else:
                for url in existing_accounts:
                    self.scrape_yt(url, url in new_accounts)

            self.yt_urls = existing_accounts.copy()

    # add account waly button pe click krne se ye function call hoga
    def add_insta_account(self,username):
        pattern = r'^[a-zA-Z0-9._]{1,30}$'
        if username == "" or not re.match(pattern, username):
            pass

        else:
            # Make a copy of the insta_accounts set
            updated_accounts = self.insta_accounts.copy()
            updated_accounts.add(username)
            # self.insta_accounts.add(username)
            with open(self.insta_accounts_file, "w") as f:
                for url in updated_accounts:
                    f.write(url + "\n")
                return True
        return False
    
    def urlCleaner(self,url):

        if '@' in url:
            split = url.split('@')
            if(len(split) == 2):
                if '/' in split[1]:
                    s2 = split[1].split('/')
                    if self.ytChecker(split[0]):

                        test = "https://www.youtube.com/" + "@" + s2[0]
                    else:
                        return -1

                    return test
                else:
                    return "https://www.youtube.com/" + "@" + split[1]
            else:
                return -2
        else:
            return -3

    def ytChecker(self,str):
        s = str.lower()
        if "youtube.com" in s.lower() :
            # print("Pehla clear")
            sp = s.split("youtube.com")
            if sp[0] == "" or sp[0].lower()== "www." or sp[0].lower()== "https://www.":
                # print("doosra clear")
                return True
            else:
                 return False
        else:
            return False 
        
    def add_yt_urls(self,username):
        cleanUrl = self.urlCleaner(username)
        # print(cleanUrl)
        if username == "" or (cleanUrl== -1):
            # print("clear")
            return False

        else:
            
            updated_accounts = self.yt_urls.copy()
            updated_accounts.add(cleanUrl)
            # self.yt_urls.add(cleanUrl)
            with open(self.yt_url_file, "w") as f:
                for url in updated_accounts:
                    f.write(url + "\n")
                return True
    def remove_emojis(self, data):
        emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002500-\U00002BEF"  # chinese char
                                u"\U00002702-\U000027B0"
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                u"\U0001f926-\U0001f937"
                                u"\U00010000-\U0010ffff"
                                u"\u2640-\u2642"
                                u"\u2600-\u2B55"
                                u"\u200d"
                                u"\u23cf"
                                u"\u23e9"
                                u"\u231a"
                                u"\ufe0f"  # dingbats
                                u"\u3030"
                                u"\U0001F000-\U0001F6FF"  # various emoji ranges
                                u"\U0001F900-\U0001F9FF"
                                u"\U0001FA70-\U0001FAFF"
                                "]+", re.UNICODE)
        return re.sub(emoji_pattern, '', data)
