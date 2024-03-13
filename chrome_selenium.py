from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import re
from selenium import webdriver
from time import sleep
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from enum import Enum
from selenium.webdriver.common.action_chains import ActionChains


class EventString(Enum):
    PAY_AGAIN_REWARD = "LỄ BAO NẠP THẺ THỜI HẠN"
    LUCKY_POINTER = 'Quay số may mắn'
    XIAOFEI_LEIJI = 'TÍCH LUỸ TIÊU PHÍ'
    DISCOUNT_ACTIVITY = 'THƯƠNG NHÂN - TÂN THẾ GIỚI'
    CARD_ACTIVITY = 'Thu thập thẻ bài'
    SUMMER_ONLINE_PRIZE = 'VUI VẺ ONLINE'
    SALE = 'HẢI TẶC ĐẤU GIÁ'
    PRESTIGE_ROULETTE = 'Vòng quay danh vọng'
    ROULETTE = 'Vòng quay kinh nghiệm'


class EventBoolean(Enum):
    PAY_AGAIN_REWARD = True  # lễ bao thời hạn
    LUCKY_POINTER = False  # quay số may mắn
    XIAOFEI_LEIJI = False  # tích lũy tiêu phí
    DISCOUNT_ACTIVITY = False  # thương nhân hải tặc
    CARD_ACTIVITY = False  # thu tập thẻ bài
    SUMMER_ONLINE_PRIZE = False  # vui vẻ online
    SALE = False  # đấu giá
    PRESTIGE_ROULETTE = True  # vòng quay danh vọng
    ROULETTE = True  # vòng quay kinh nghiệm


def perform_action(driver, link_id, button_id, wait):
    sleep(2)
    link = wait.until(EC.presence_of_element_located((By.ID, link_id)))
    link.click()
    sleep(0.5)
    button = wait.until(EC.presence_of_element_located((By.ID, button_id)))
    button.click()
    handle_alert(driver)


def handle_alert(driver, timeout=10):
    try:
        # Chờ cho cảnh báo xuất hiện
        alert = WebDriverWait(driver, timeout).until(EC.alert_is_present())
        # Chuyển sang cửa sổ cảnh báo
        alert = driver.switch_to.alert
        # Chấp nhận cảnh báo (ấn OK)
        alert.accept()
        print("Đã ấn OK trong cảnh báo.")
    except TimeoutException:
        print("Không có cảnh báo nào xuất hiện.")


chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)

sleep(1)

pyautogui.hotkey('win', 'up')
pyautogui.click(pyautogui.position(410, 70))  # click url
pyautogui.write("http://article.haitacviet.com/wp-login.php")
pyautogui.press("enter")
# sleep(2)
# wait login
sleep(0.5)
waitLogin = WebDriverWait(driver, 10)
# elementSubmit = waitLogin.until(EC.presence_of_element_located((By.ID, "wp-submit")))

username_input = waitLogin.until(EC.presence_of_element_located((By.ID, "user_login")))
username_input.send_keys("haitacviet")

password_input = driver.find_element(By.ID, "user_pass")
password_input.send_keys("Devviet@2017")

login_button = driver.find_element(By.ID, "wp-submit")
login_button.click()

# pyautogui.click(pyautogui.position(1070, 680))  # click login
sleep(1)
wait = WebDriverWait(driver, 10)
elementPosts = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='menu-posts']/a/div[3]")))
elementPosts.click()

stringEvent = '[Event/HĐ] Chuỗi Event Hoạt Động'
target_elements = driver.find_elements(By.XPATH, f"//a[contains(@aria-label, '{stringEvent}') and text()='Xem thử']")

# Scroll đến phần tử
# driver.execute_script("arguments[0].scrollIntoView(true);", target_elements[0])
driver.execute_script("arguments[0].click();", target_elements[0])
sleep(1)
#  set value start_date , end_date
start_date = ''
end_date = ''
paragraphs = driver.find_elements(By.TAG_NAME, 'strong')
# for event in paragraphs:
#     if event.text == EventString.XIAOFEI_LEIJI:
#         EventBoolean.XIAOFEI_LEIJI = True
#     if event.text == EventString.DISCOUNT_ACTIVITY:
#         EventBoolean.DISCOUNT_ACTIVITY = True
#     if event.text == EventString.LUCKY_POINTER:
#         EventBoolean.LUCKY_POINTER = True
#     if event.text == EventString.CARD_ACTIVITY:
#         EventBoolean.CARD_ACTIVITY = True
#     if event.text == EventString.SUMMER_ONLINE_PRIZE:
#         EventBoolean.SUMMER_ONLINE_PRIZE = True
#     if event.text == EventString.SALE:
#         EventBoolean.SALE = True

for element in paragraphs:
    if 'ngày' in element.text:
        dates = re.findall(r'\d{2}/\d{2}/\d{4}', element.text)
        start_date = datetime.strptime(dates[0].replace(" ", ""), "%d/%m/%Y").strftime("%Y-%m-%d")
        end_date = datetime.strptime(dates[1].replace(" ", ""), "%d/%m/%Y").strftime("%Y-%m-%d")
        print(start_date, end_date)
        break

# ---- open visual studio
sleep(1)
pyautogui.press('win')
pyautogui.write("Visual studio")
pyautogui.press('enter')
pyautogui.moveTo(1111, 503)
sleep(3)
pyautogui.rightClick()
sleep(1)
pyautogui.moveTo(1150, 589)
pyautogui.click()
# ------
# ----
driver.get("http://localhost:3000/index.php")
driver.execute_script("localStorage.setItem('start_date', arguments[0]);", start_date)
driver.execute_script("localStorage.setItem('end_date', arguments[0]);", end_date)
driver.execute_script("location.reload();")
sleep(1)
# ✌️ prestige_roulette
perform_action(driver, "prestige_roulette_link", "submit_button_prestige_roulette", wait)
# ✌️ roulette
perform_action(driver, "roulette_link", "submit_button_roulette", wait)
# ✌️ Pay again reward
perform_action(driver, "payAgainreward_link", "submit_button_payagainreward", wait)

sleep(100)
