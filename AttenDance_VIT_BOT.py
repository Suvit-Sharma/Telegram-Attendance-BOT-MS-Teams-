from telegram import *
from telegram.ext import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

# enter your own email ID in double qoutes
email_id = ""
# Enter your password in double quotes
passcode = ""

opt = Options()
# for heroku 4 line
# opt.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# opt.add_argument('--headless')
# opt.add_argument('--no-sandbox')
# opt.add_argument('--disable-dev-shm-usage')
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 2, 
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.geolocation": 2, 
    "profile.default_content_setting_values.notifications": 2 
  })



bot = Bot("1656078007:AAG3R77h_Izw4z-wWo8XigAX8Iw5Io3Jfyg")
updater = Updater("1656078007:AAG3R77h_Izw4z-wWo8XigAX8Iw5Io3Jfyg", use_context=True)

dispatcher = updater.dispatcher

list_subject=[]
# for normal usage
driver = webdriver.Chrome(options=opt, executable_path="C:\\Users\\HP\\PycharmProjects\\Whatsapp_Tracker\\chromedriver.exe")
# for heroku
# driver = webdriver.Chrome(options=opt, executable_path=os.environ.get("CHROMEDRIVER_PATH"))
print("app started")
def select_subject(user_input):
    driver.find_element_by_xpath("//h1[contains(normalize-space(text()),'{}')]".format(list_subject[int(user_input)-1])).click()
    time.sleep(10)
    driver.find_element_by_xpath("//span[contains(text(),'Join')]").click()
    time.sleep(10)
    driver.find_element_by_xpath("//button[contains(text(),'Continue without audio or video')]").click()
    time.sleep(10)
    driver.find_element_by_xpath("//button[contains(text(),'Join now')]").click()


def reply(update, context):
    user_input = update.message.text
    update.message.reply_text(select_subject(user_input))

def intro(update:Update,CallbackContext:CallbackContext):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text = "Wese attend kar lete to accha hota, chalo koi na !!!"
    )


    # driver = webdriver.Chrome(executable_path="C:\\Users\\HP\\PycharmProjects\\Whatsapp_Tracker\\chromedriver.exe")
    driver.get("https://login.microsoftonline.com/common/oauth2/authorize?response_type=id_token&client_id=5e3ce6c0-2b1f-4285-8d4b-75ee78787346&redirect_uri=https%3A%2F%2Fteams.microsoft.com%2Fgo&state=a4dd8312-e2ae-4ca1-bf41-96f10e6c9cfa&&client-request-id=8f105393-d6e6-4b7f-92bf-7ae5603a9ddb&x-client-SKU=Js&x-client-Ver=1.0.9&nonce=3e452ba3-0343-4db2-8887-1fd4782a1daa&domain_hint=")
    driver.implicitly_wait(40)
    driver.find_element_by_xpath("/html/body/div/form[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/input[1]").send_keys(email_id)
    driver.find_element_by_xpath("//*[@id='idSIButton9']").click()
    driver.find_element_by_xpath("/html/body/div/form[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/input").send_keys(passcode)
    driver.find_element_by_xpath("/html/body/div/form[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div/div/input").click()
    driver.find_element_by_xpath("/html/body/div/form/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input").click()

    all_clases = driver.find_elements_by_xpath("//h1[contains(@class,'team-name-text')]")

    global list_subject
    for _ in all_clases:
        list_subject.append(_.text)
    print(list_subject)
    string_subject = ""
    count = 1
    for _ in list_subject:
        string_subject += str(count) + " - " + str(_) + "\n"
        count+=1
    bot.send_message(
        chat_id=update.effective_chat.id,
        text= string_subject
    )
        

start_value = CommandHandler("start", intro)
dispatcher.add_handler(start_value)
dispatcher.add_handler(MessageHandler(Filters.text, reply))




updater.start_polling()