# Action Chain
import time
import os
import datetime
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from inputimeout import inputimeout


# Set up ChromeOptions
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Add user-agent to ChromeOptions
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Add additional options to mimic human-like behavior
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Create a Chrome driver instance with ChromeOptions
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the specified webpage
url = 'https://service.berlin.de/dienstleistung/120686/'

# Use WebDriverWait to wait for the page to load
wait = WebDriverWait(driver, 10)  # Increased timeout to 10 seconds

# Times of loop
x = 0
new_row = [
    [0,0]
]

# Create database with list with zero.
data_base = [
    [0, 0]
]

# Function for the notification for Mac
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

# It needs to loop forever
while True:

    # Open the webpage
    driver.get(url)
    print('Loop Number',x+1, 'starts')
    print("Successfully opened the webpage")

    driver.execute_script("window.scrollTo(0, 500)")

    time.sleep(3)

    # Find the button of "Terminbuchung"
    button_termin = driver.find_element(By.XPATH, '//*[@id="layout-grid__area--maincontent"]/div[2]/div[3]/a')
    button_termin.click()

    # Find the key word "Bitte wählen Sie ein Datum" on the page
    get_source = driver.page_source
    search_text = "Bitte wählen Sie ein Datum"

    # Note: The find() method returns the index of first occurrence of the substring (if found). If not found, it returns -1.
    if get_source.find(search_text) >0:
        print('Log in succeeded appointment found at', datetime.datetime.now())
        k = "Succeeded"
        j = str(datetime.datetime.now())
        notify("Hey", "Appointment is available now!!!")

        try:
            # Take timed input using inputimeout() function
            time_over = inputimeout(prompt='Skip or not?', timeout=120)

            # Catch the timeout error
        except Exception:

            # Declare the timeout statement
            time_over = 'Time is over. We will skip and loop again.'
            print(time_over)

    else:
        print("Log in failed at: ", datetime.datetime.now())
        k = "Failed"
        j = str(datetime.datetime.now())

    # Insert the values into the database
    data_base[x][0] = k
    data_base[x][1] = j
    print('Loop Number', x+1, k, 'and', k, 'time at', datetime.datetime.now())
    print(data_base)

    # Add one new row to the database
    x = x +1
    data_base = np.append(data_base, new_row, axis=0)

    # Create waiting time to mini human behavior
    n = 1
    while True:
        time.sleep(1)
        n = n+1
        print(n)
        if n == 10:
            break
