import json
import os
import time
from datetime import timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

WINDOW_SIZE = (1920, 953)

def load_config():
    try:
        with open("./config.json", "r") as c:
            config = json.load(c)
    except:
        with open("./config.json", 'w') as c:
            json.dump({
                "url": "http://moodle-cdo.kemsu.ru/login/index.php",
                "username": "",
                "password": "",
                "course_title": "ГЕОИНФОРМАТИКА",
                "theme_string": "Знакомство с ГИС- системами"
            }, c, indent=4, ensure_ascii=False)
            print(f"Конфиг не найден\nСоздан {os.path.join(os.getcwd(), "config.json")}, введите туда недостающие данные")
            exit(1)
    return config

def setup_driver():
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--headless")
    options.add_argument(f"--window-size={WINDOW_SIZE[0]},{WINDOW_SIZE[1]}")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

def open_page(driver, config):
    driver.get(config["url"])

    field_login = driver.find_element(By.ID, "username")
    field_password = driver.find_element(By.ID, "password")
    btn_login = driver.find_element(By.ID, "loginbtn")

    field_login.send_keys(config["username"])
    field_password.send_keys(config["password"])
    btn_login.click()

    try:
        driver.find_element(By.CLASS_NAME, "usertext")
        print("logged in")
    except:
        driver.get_screenshot_as_file("./screen.png")
        print(f"Что-то пошло не так, проверьте {os.path.join(os.getcwd(), "screen.png")}")

    driver.find_element(By.LINK_TEXT, config["course_title"]).click()

    try:
        driver.find_element(By.XPATH, f"//*[contains(text(), '{config["theme_string"]}')]")
        print("succ ess")
    except:
        driver.get_screenshot_as_file("./screen.png")
        print(f"Что-то пошло не так, проверьте {os.path.join(os.getcwd(), "screen.png")}")

def keep_alive():
    print("\nвремя сессии - time\nобновить страницу - refresh\nсделать скриншот - screen\nвыйти - exit")
    start = time.time()
    while True:
        a = input()
        if "exit" in a:
            exit()
        elif "refresh" in a:
            driver.refresh()
        elif "screen" in a:
            driver.get_screenshot_as_file("./screen.png")
            print(f"скриншот сохранен {os.path.join(os.getcwd(), "screen.png")}")
        elif "time" in a:
            print(f"прошло {timedelta(seconds=time.time() - start)}")
        else:
            continue

if __name__ == "__main__":
    config = load_config()
    driver = setup_driver()
    
    open_page(driver, config)
    keep_alive()
