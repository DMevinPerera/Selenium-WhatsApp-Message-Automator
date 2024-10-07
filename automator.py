from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
import os

# Set Chrome options
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")  # Ensure this path is correct for your OS

os.system("")
os.environ["WDM_LOG_LEVEL"] = "0"

class style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

print(style.BLUE)
print("**********************************************************")
print("**********************************************************")
print("*****                                               ******")
print("*****  THANK YOU FOR USING WHATSAPP BULK MESSENGER  ******")
print("*****      This tool was built by Anirudh Bagri     ******")
print("*****           www.github.com/anirudhbagri         ******")
print("*****                                               ******")
print("**********************************************************")
print("**********************************************************")
print(style.RESET)

# Read message from file
with open("message.txt", "r", encoding="utf8") as f:
    message = f.read()

print(style.YELLOW + '\nThis is your message-')
print(style.GREEN + message)
print("\n" + style.RESET)
message = quote(message)

# Read numbers from file
numbers = []
with open("numbers.txt", "r") as f:
    for line in f.read().splitlines():
        if line.strip():
            numbers.append(line.strip())

total_number = len(numbers)
print(style.RED + 'We found ' + str(total_number) + ' numbers in the file' + style.RESET)
delay = 30

# Initialize the WebDriver with the correct Service object
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print('Once your browser opens up, sign in to web WhatsApp.')
driver.get('https://web.whatsapp.com')

input(style.MAGENTA + "AFTER logging into WhatsApp Web is complete and your chats are visible, press ENTER..." + style.RESET)

max_retries = 3  # Set the maximum number of retry attempts
delay_between_retries = 5  # Time to wait before retrying (in seconds)

# Sending messages
for idx, number in enumerate(numbers):
    number = number.strip()
    if not number:
        continue

    print(style.YELLOW + '{}/{} => Sending message to {}.'.format((idx + 1), total_number, number) + style.RESET)

    retries = 0  # Initialize the retry counter

    while retries < max_retries:
        try:
            url = f'https://web.whatsapp.com/send?phone={number}&text={message}'
            driver.get(url)

            # Wait for the message input box to be present using CSS_SELECTOR
            input_box = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']")))

            # Click to focus on the input box
            input_box.click()
            input_box.send_keys(message)  # Type the message

            # Wait for the send button using the provided CSS_SELECTOR
            send_button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#main > footer > div.x1n2onr6.xhtitgo.x9f619.x78zum5.x1q0g3np.xuk3077.x193iq5w.x122xwht.x1bmpntp.xy80clv.xgkeump.x26u7qi.xs9asl8.x1swvt13.x1pi30zi.xnpuxes.copyable-area > div > span:nth-child(2) > div > div._ak1r > div.x123j3cw.xs9asl8.x9f619.x78zum5.x6s0dn4.xl56j7k.x1ofbdpd.x100vrsf.x1fns5xo > button')))

            # Optional: Add a brief sleep to ensure the UI is ready
            sleep(1)

            # Click the send button using JavaScript
            driver.execute_script("arguments[0].click();", send_button)

            sleep(3)  # Wait for the message to be sent
            print(style.GREEN + 'Message sent to: ' + number + style.RESET)
            break  # Exit the retry loop if successful

        except Exception as e:
            retries += 1
            print(style.RED + f"Failed to send message to {number} (Attempt {retries}/{max_retries}): {e}" + style.RESET)

            if retries < max_retries:
                print(style.YELLOW + f"Retrying... ({retries}/{max_retries})" + style.RESET)
                sleep(delay_between_retries)  # Wait before retrying
            else:
                print(style.RED + f"Giving up on {number} after {retries} failed attempts." + style.RESET)

# Close the browser after sending messages
driver.quit()