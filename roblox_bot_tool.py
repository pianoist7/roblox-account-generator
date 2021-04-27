import time
import random
import string

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


class AccountGenerationTool: #don't change anything in here

    username, password = "", ""
    gender = ""
    birthday_day, birthday_month, birthday_year = "", "", ""

    DEBUG_FILE_NAME = time.strftime("Debug-%H.%M.%S.log", time.gmtime())  # name of the debug file
    OUTPUT_FILE_NAME = "accounts"  # name of the folder in which information about the accounts is stored

    NUMBER_OF_ACCOUNTS = 1  # number of accounts to create
    USERNAME_LENGTH = 20  # length of the username, cannot be greater than 20

    SUCCESS_URL = "https://www.roblox.com/home?nu=true"  # url to which the browser will be redirected if success
    PROXY_IP = "51.158.172.165:8761"  # using a proxy is well-advised
    PROXY_ENABLED = True

    ATTEMPT_LIMIT = 5  # maximum number of attempts to carry out in case of failed attempt
    DEFAULT_WAIT_TIME = 5  # time to wait in between each attempt

    MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

    def __init__(self):
        for i in range(self.NUMBER_OF_ACCOUNTS):
            self.setup_user()
            self.create_user()

    def log(self, message):
        open(file=self.DEBUG_FILE_NAME, mode="a").write(f"{message}\n")

    def generate_username(self, chars=string.ascii_uppercase + string.digits):
        return "".join(random.choice(chars) for _ in range(self.USERNAME_LENGTH))

    def setup_user(self): #setting up the account - username, password, gender and birthday y/m/d
        self.username = self.generate_username()
        self.password = self.username[::-1]
        self.gender = "Male" if random.randint(0, 1) == 1 else "Female"

        self.birthday_year = random.randint(1922, 2004)
        self.birthday_month = self.MONTHS[random.randint(0, 11)]
        self.birthday_day = random.randint(1, 32)

    def create_user(self):

        # set up the driver
        options = Options()
        if self.PROXY_ENABLED:
            options.add_argument(f"--proxy-server={self.PROXY_IP}")

        # start the driver
        browser = webdriver.Chrome("chromedriver.exe", options=options)

        # only connect the first time to avoid superfluous requests
        if browser.current_url != "https://www.roblox.com":
            browser.get("https://www.roblox.com")

        # locate and lock onto the elements of the home page
        username_input_box = browser.find_element_by_name("signupUsername")
        password_input_box = browser.find_element_by_name("signupPassword")
        gender_icon = browser.find_element_by_name(f"gender{self.gender}")
        day_dropdown_list = browser.find_element_by_name("birthdayDay")
        month_dropdown_list = browser.find_element_by_name("birthdayMonth")
        year_dropdown_list = browser.find_element_by_name("birthdayYear")
        signup_button = browser.find_element_by_name("signupSubmit")

        # set the birthdate
        Select(month_dropdown_list).select_by_value(self.birthday_month)
        Select(day_dropdown_list).select_by_value(
            f"0{self.birthday_day}" if self.birthday_day < 10 else str(self.birthday_day))
        Select(year_dropdown_list).select_by_value(str(self.birthday_year))

        # uses the values and names assigned before, clicks and types in boxes
        username_input_box.send_keys(self.username)
        password_input_box.send_keys(self.password)
        gender_icon.click()
        time.sleep(0.1)  # a brief delay is required
        signup_button.click()

        # reset the counter for each account and reset current url
        current_url = browser.current_url
        attempts = 0

        # send requests to the server until successful registration
        while self.SUCCESS_URL not in current_url and attempts < self.ATTEMPT_LIMIT:

            # put the 2captcha client here

            # wait some time before attempting another request
            time.sleep(self.DEFAULT_WAIT_TIME)

            # log the attempt in a debug file
            current_url = browser.current_url
            self.log(f"Attempt {attempts} out of {self.ATTEMPT_LIMIT}.")

            attempts += 1

        # look for a successful registration for each attempt
        if self.SUCCESS_URL in current_url:

            # created account successfully
            print("Account created successfully.")

            # write account data in file
            open(file=f"{self.OUTPUT_FILE_NAME}.txt", mode="a").write(f"{self.username}:{self.password}\n")

            # log out of the account to avoid redirection towards the home page on the next iteration
            browser.find_element_by_class_name("icon-nav-settings roblox-popover-close").click()
            browser.find_element_by_class_name("rbx-menu-item logout-menu-item").click()
            browser.find_element_by_class_name("change-email-button").click()

        else:

            # failed creating account
            print(f"Account could not be created, terminating process.")
        browser.quit()


if __name__ == "__main__":
    f = AccountGenerationTool()
