# whatsapp bot without website detection
"""
todo
instead of time.sleep, expected conditions can be used.
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
import datetime
import time

# name of contact to listen commands
contact = "contact_name"
#               /home/<USER>/.mozilla/firefox/<PROFILE DIRECTORY>
profile_path = "/home/tfp/.mozilla/firefox/nm7hly0v.selenium"

# some settings for app
message_check_intervals = 10  # seconds
maximum_repeat = 10  # to check.
#              ex 3600 for 10 hours

# initialize whatsapp web
# exec_path = "/home/tfp/Documents/geckodriver"
# using gecko driver manager instead of direct path. because it's prone to errors
profile = webdriver.FirefoxProfile(profile_path)
exec_path = GeckoDriverManager().install()
driver = webdriver.Firefox(executable_path=exec_path, firefox_profile=profile)
driver.get("https://web.whatsapp.com/")

# to store latest commands and to react accordingly, using list container
recent_messages_list = []


def command_hello():
    if "Hi. This message was sent automatically." in recent_messages_list:
        pass
    else:
        send_message("Hi. This message was sent automatically.")


def click_on_contact(contact_name):
    # search and click on contact
    try:
        # click on search box
        # input_box_search = driver.find_element_by_class_name("_2EoyP")
        input_box_search = driver.find_element_by_xpath('//div[@data-tab="3"]')
        input_box_search.click()
        time.sleep(2)

        # search for contact
        input_box_search.send_keys(contact_name)
        time.sleep(2)

        # click on contact
        selected_contact = driver.find_element_by_xpath("//span[@title='" + contact_name + "']")
        selected_contact.click()

    # if it can't find, it'll let you handle
    except NoSuchElementException as e:
        print("couldn't find. exception: {}".format(e))
    else:
        print("contact has been selected.")


def send_message(text):
    # try sending messages
    try:
        input_box = driver.find_element_by_xpath('//div[@data-tab="6"]')
        time.sleep(2)

        # write and send the message
        input_box.send_keys(text + Keys.ENTER)
        time.sleep(2)

    # if it can't find, it'll let you handle
    except NoSuchElementException as e:
        print("couldn't find. exception: {}".format(e))


def check_recent_messages():
    # clearing messages from past calls
    recent_messages_list.clear()
    # using datetime to make it usable all the time
    now = str(datetime.datetime.now())
    last_minute = str(datetime.datetime.now() - datetime.timedelta(minutes=1))
    year = int(now[0:4])
    month = int(now[5:7])
    day = int(now[8:10])
    hour = now[11:16]
    hour_minus_1 = last_minute[11:16]
    try:
        # it will try to find messages in that minute
        sent_message = driver.find_elements_by_xpath("//div[contains(@data-pre-plain-text, '[{}, {}/{}/{}]')]".format(hour, month, day, year))
        if len(sent_message) == 0:
            print("no recent messages. trying minus 1 minute")
            time.sleep(0.5)
            # if it can't find it'll try to find minute before
            sent_message = driver.find_elements_by_xpath(
                "//div[contains(@data-pre-plain-text, '[{}, {}/{}/{}]')]".format(hour_minus_1, month, day, year))
            if len(sent_message) == 0:
                print("  no recent messages on minus 1 minute\n"
                      "------------------------------------------\n")
            else:
                for j in sent_message:
                    print("found message: {}".format(j.text))
                    recent_messages_list.append(j.text)
        else:
            for m in sent_message:
                print("found message: {}".format(m.text))
                recent_messages_list.append(m.text)
    except NoSuchElementException as e:
        print("couldn't find. exception: {}".format(e))


def respond_to_command():
    # checking if there are commands
    for c in recent_messages_list:
        if c == "!hello":
            print("     found a command")
            command_hello()


time.sleep(5)  # sometimes it can take some time to load whatsapp
click_on_contact(contact)
print("detection loop has started\n")

for i in range(maximum_repeat):  # using for loop to find commands
    time.sleep(message_check_intervals)
    print("     try {}".format(i+1))
    check_recent_messages()
    time.sleep(0.5)
    respond_to_command()

input("script has finished press enter to quit\n")
driver.quit()
