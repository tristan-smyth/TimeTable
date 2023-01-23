from fastapi import FastAPI

app = FastAPI()

from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

@app.get("/")
def home():
    return {"Test"}

@app.get("/data/{department}/{student_group}")
def get_driver(department: int=8,student_group: int=13,delay=0, debug=False):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.

    # Creates a new driver instance
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
    driver.get("https://timetables.dkit.ie/studentset.php")

    time.sleep(0.5)

    # --- First Page Handling ---
    # Selects EEME-Electronics & Mechanical Engineering from dropdown
    driver.find_element(By.XPATH,
                        f'/html/body/center/center/table[1]/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/select/option[{department}]').click()

    # Selects Electronic & Elec Sys Year 2 - Group2b from dropdown
    driver.find_element(By.XPATH,
                        f'/html/body/center/center/table[1]/tbody/tr[2]/td/form/table/tbody/tr[4]/td[2]/select/option[{student_group}]').click()

    # Selects the list view
    driver.find_element(By.XPATH,
                        "/html/body/center/center/table[1]/tbody/tr[2]/td/form/table/tbody/tr[5]/td[2]/select/option[2]").click()

    # Clicks the view time table button
    driver.find_element(By.XPATH,
                        '/html/body/center/center/table[1]/tbody/tr[2]/td/form/table/tbody/tr[9]/td/input').click()

    # Accepts the popup
    alert_obj = driver.switch_to.alert
    alert_obj.accept()

    time.sleep(0.5)

    # --- Second Page Handling ---
    # Selects timetable tab
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)

    # --- Data Handling ---
    # Gets Days Data
    monday = driver.find_element(By.XPATH, "/html/body/table[7]").find_elements(By.TAG_NAME, "tr")
    tuesday = driver.find_element(By.XPATH, "/html/body/table[8]").find_elements(By.TAG_NAME, "tr")
    wednesday = driver.find_element(By.XPATH, "/html/body/table[9]").find_elements(By.TAG_NAME, "tr")
    thursday = driver.find_element(By.XPATH, "/html/body/table[10]").find_elements(By.TAG_NAME, "tr")
    friday = driver.find_element(By.XPATH, "/html/body/table[11]").find_elements(By.TAG_NAME, "tr")

    # Days List definitions
    monday_lst = []
    tuesday_lst = []
    wednesday_lst = []
    thursday_lst = []
    friday_lst = []

    # Puts Monday Data and puts it into a list
    for row in range(len(monday)):
        monday_lst.append([])
        tr = monday[row].find_elements(By.TAG_NAME, "td")

        for item in tr:
            monday_lst[row].append(item.text)

    # Puts Tuesday Data and puts it into a list
    for row in range(len(tuesday)):
        tuesday_lst.append([])
        tr = tuesday[row].find_elements(By.TAG_NAME, "td")

        for item in tr:
            tuesday_lst[row].append(item.text)

    # Puts Wednesday Data and puts it into a list
    for row in range(len(wednesday)):
        wednesday_lst.append([])
        tr = wednesday[row].find_elements(By.TAG_NAME, "td")

        for item in tr:
            wednesday_lst[row].append(item.text)

    # Puts Thursday Data and puts it into a list
    for row in range(len(thursday)):
        thursday_lst.append([])
        tr = thursday[row].find_elements(By.TAG_NAME, "td")

        for item in tr:
            thursday_lst[row].append(item.text)

    # Puts Friday Data and puts it into a list
    for row in range(len(friday)):
        friday_lst.append([])
        tr = friday[row].find_elements(By.TAG_NAME, "td")

        for item in tr:
            friday_lst[row].append(item.text)

    if debug:
        for i in monday_lst:
            print(i)
        print("\n")
        for i in tuesday_lst:
            print(i)
        print("\n")
        for i in wednesday_lst:
            print(i)
        print("\n")
        for i in thursday_lst:
            print(i)
        print("\n")
        for i in friday_lst:
            print(i)

    if delay > 0:
        time.sleep(delay)

    return monday_lst,tuesday_lst,wednesday_lst,thursday_lst,friday_lst
