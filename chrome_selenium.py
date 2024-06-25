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
import subprocess
import tkinter as tk
from tkinter import messagebox


class EventString(Enum):
    PAY_AGAIN_REWARD = "LỄ BAO NẠP THẺ THỜI HẠN"
    LUCKY_POINTER = 'Quay số may mắn'
    XIAOFEI_LEIJI = 'TÍCH LUỸ TIÊU PHÍ'
    DISCOUNT_ACTIVITY = 'THƯƠNG NHÂN - TÂN THẾ GIỚI'
    CARD_ACTIVITY = 'THU THẬP THẺ BÀI'
    SUMMER_ONLINE_PRIZE = 'VUI VẺ ONLINE'
    SALE = 'HẢI TẶC ĐẤU GIÁ (ĐẤU GIÁ MINI)'
    PRESTIGE_ROULETTE = 'Vòng quay danh vọng'
    ROULETTE = 'Vòng quay kinh nghiệm'
    JIERI_SHOP = 'THƯƠNG THÀNH TÍCH LUỸ'
    GUAGUALE = 'CÀO TRÚNG THƯỞNG'


event_booleans = {
    "PAY_AGAIN_REWARD": True,  # lễ bao thời hạn
    "LUCKY_POINTER": False,  # quay số may mắn
    "XIAOFEI_LEIJI": False,  # tích lũy tiêu phí
    "DISCOUNT_ACTIVITY": False,  # thương nhân hải tặc
    "CARD_ACTIVITY": False,  # thu tập thẻ bài
    "SUMMER_ONLINE_PRIZE": False,  # vui vẻ online
    "SALE": False,  # đấu giá
    "PRESTIGE_ROULETTE": True,  # vòng quay danh vọng
    "ROULETTE": True,  # vòng quay kinh nghiệm
    "JIERI_SHOP": False,  # thương thành tích lũy
    "GUAGUALE": False  # cào trúng thưởng
}


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
pyautogui.write("http://article.oplegend.com/wp-login.php")
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

sleep(1)
# Scroll đến phần tửs
# driver.execute_script("arguments[0].scrollIntoView(true);", target_elements[0])
driver.execute_script("arguments[0].click();", target_elements[0])
#  set value start_date , end_date
start_date = ''
end_date = ''
paragraphs = driver.find_elements(By.TAG_NAME, 'strong')

for element in paragraphs:
    if 'ngày' in element.text:
        dates = re.findall(r'\d{2}/\d{2}/\d{4}', element.text)
        start_date = datetime.strptime(dates[0].replace(" ", ""), "%d/%m/%Y").strftime("%Y-%m-%d")
        end_date = datetime.strptime(dates[1].replace(" ", ""), "%d/%m/%Y").strftime("%Y-%m-%d")
        print(start_date, end_date)
        # file.write(f"End Date: {end_date}\n")
        # print("Dates have been written to dates.txt")
        break

with open('C:\\auto_config_event\\sukien\\ajax\\date.txt', 'w') as file:
    file.write(start_date + " " + end_date + "\n")
    for event in paragraphs:
        if EventString.XIAOFEI_LEIJI.value in event.text:
            event_booleans["XIAOFEI_LEIJI"] = True
            file.write("XIAOFEI_LEIJI\n")
        if EventString.DISCOUNT_ACTIVITY.value in event.text:
            event_booleans["DISCOUNT_ACTIVITY"] = True
            file.write("DISCOUNT_ACTIVITY\n")
        if EventString.LUCKY_POINTER.value in event.text:
            event_booleans["LUCKY_POINTER"] = True
            file.write("LUCKY_POINTER\n")
        if EventString.CARD_ACTIVITY.value in event.text:
            event_booleans["CARD_ACTIVITY"] = True
            file.write("CARD_ACTIVITY\n")
        if EventString.SUMMER_ONLINE_PRIZE.value in event.text:
            event_booleans["SUMMER_ONLINE_PRIZE"] = True
            file.write("SUMMER_ONLINE_PRIZE\n")
        if EventString.SALE.value in event.text:
            event_booleans["SALE"] = True
            file.write("SALE\n")
        if EventString.JIERI_SHOP.value in event.text:
            event_booleans["JIERI_SHOP"] = True
            file.write("JIERI_SHOP\n")
        if EventString.GUAGUALE.value in event.text:
            event_booleans["GUAGUALE"] = True
            file.write("GUAGUALE\n")
        print(event.text)
    print("Dates have been written to dates.txt")

subprocess.call(['php', 'C:\\auto_config_event\\sukien\\ajax\\aaa.php'])

#
# --------- open visual studio
# sleep(1)
# pyautogui.press('win')
# pyautogui.write("Visual studio")
# pyautogui.press('enter')
# pyautogui.moveTo(1111, 503)
# sleep(3)
# pyautogui.rightClick()
# sleep(1)
# pyautogui.moveTo(1150, 589)
# pyautogui.click()
# ------
# ------ open web server
project_directory = r'C:\auto_config_event\sukien'


subprocess.Popen(['php', '-S', 'localhost:3000'], cwd=project_directory)
sleep(1)
# ----
driver.get("http://localhost:3000/index.php")
driver.execute_script("localStorage.setItem('start_date', arguments[0]);", start_date)
driver.execute_script("localStorage.setItem('end_date', arguments[0]);", end_date)
driver.execute_script("location.reload();")

# # ✌️ PRESTIGE_ROULETTE
# perform_action(driver, "prestige_roulette_link", "submit_button_prestige_roulette", wait)
#
# # ✌️ ROULETTE
# perform_action(driver, "roulette_link", "submit_button_roulette", wait)
#
# ✌️ PAY AGAIN REWARD
# perform_action(driver, "payAgainreward_link", "submit_button_payagainreward", wait)
linkPayAgain = wait.until(EC.presence_of_element_located((By.ID, "payAgainreward_link")))
linkPayAgain.click()
#
# # ✌️ SUMMER ONLINE PRIZE
# if event_booleans["SUMMER_ONLINE_PRIZE"]:
#     perform_action(driver, "summer_online_prize_link", "submit_button_summeronlineprize", wait)
#
# # ✌️ CARD ACTIVITY
# if event_booleans["CARD_ACTIVITY"]:
#     perform_action(driver, "card_activity_link", "submit_button_cardactivity", wait)
#
# # ✌️ LUCKY_POINTER
# if event_booleans["LUCKY_POINTER"]:
#     perform_action(driver, "luckyPointer_link", "submit_button_LuckyPointer", wait)
#
# # ✌️ DISCOUNT_ACTIVITY
# if event_booleans["DISCOUNT_ACTIVITY"]:
#     perform_action(driver, "discount_activity_link", "submit_button_discountactivity", wait)
#
# # ✌️ XIAOFEI_LEIJI
# if event_booleans["XIAOFEI_LEIJI"]:
#     perform_action(driver, "xiaofei_leiji_link", "submit_button_xiaofeileiji", wait)
#
# # ✌️ JIERI_SHOP
# if event_booleans["JIERI_SHOP"]:
#     perform_action(driver, "jieri_shop_link", "submit_button_jierishop", wait)
#
# # ✌️ SALE
# if event_booleans["SALE"]:
#     perform_action(driver, "sale_link", "submit_button_sale", wait)
#
# # ✌️ OBT_ACTIVITY
# sleep(2)
# obt_activity_link = wait.until(EC.presence_of_element_located((By.ID, "obtActivity_link")))
# obt_activity_link.click()
# sleep(0.5)
# if event_booleans["DISCOUNT_ACTIVITY"]:
#     checkbox_element = wait.until(EC.presence_of_element_located((By.ID, "checkbox_discount_activity")))
#     driver.execute_script("arguments[0].checked = true;", checkbox_element)
# if event_booleans["JIERI_SHOP"]:
#     checkbox_element = wait.until(EC.presence_of_element_located((By.ID, "checkbox_jieri_shop")))
#     driver.execute_script("arguments[0].checked = true;", checkbox_element)
# if event_booleans["SUMMER_ONLINE_PRIZE"]:
#     checkbox_element = wait.until(EC.presence_of_element_located((By.ID, "checkbox_summer_online_prize")))
#     driver.execute_script("arguments[0].checked = true;", checkbox_element)
# if event_booleans["XIAOFEI_LEIJI"]:
#     checkbox_element = wait.until(EC.presence_of_element_located((By.ID, "checkbox_xiaofei_leiji")))
#     driver.execute_script("arguments[0].checked = true;", checkbox_element)
# if event_booleans["CARD_ACTIVITY"]:
#     checkbox_element = wait.until(EC.presence_of_element_located((By.ID, "checkbox_card_activity")))
#     driver.execute_script("arguments[0].checked = true;", checkbox_element)
# if event_booleans["LUCKY_POINTER"]:
#     checkbox_element = wait.until(EC.presence_of_element_located((By.ID, "checkbox_lucky_pointer")))
#     driver.execute_script("arguments[0].checked = true;", checkbox_element)
# sleep(0.5)
# button_obt_activity = wait.until(EC.presence_of_element_located((By.ID, "submit_button_obtactivity")))
# button_obt_activity.click()
# handle_alert(driver)
#


# sleep(100)
sleep(1000)