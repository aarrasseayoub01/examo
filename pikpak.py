import os
import threading
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time
import requests
import webbrowser
import wget
import json

login_url = "https://mypikpak.com/drive/login"

credentials = {
    "token_type": "Bearer", "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjM5Y2Q4ZTdjLTUyNGQtNDM5ZC04MzY0LTFjMzA2YzliNTc2NiJ9.eyJpc3MiOiJodHRwczovL3VzZXIubXlwaWtwYWsuY29tIiwic3ViIjoiWTBNOFJTV3NQRE1fcU1mNiIsImF1ZCI6IllVTXg1bkk4WlU4QXA4cG0iLCJleHAiOjE2Njk1OTQzMDgsImlhdCI6MTY2OTU4NzEwOCwiYXRfaGFzaCI6InIuZlFWTklHNmdFZTJSMVBwS25PS0V0QSIsInNjb3BlIjoicGFuIHVzZXIgb2ZmbGluZSIsInByb2plY3RfaWQiOiIyd2tzNTZjMzFkYzgwc3htNXA5In0.W3y0QBJjeQH1uEbfOIRMcwrJ-AXdlRkYBbe7e6MisMmWEJMNuiqSais8ahMSwME_MSgOlsX2hFeuxe4TrhU1TsDy4ok1_KuDjXci9CqgRRjQ7lqcm07tOuoukEexGDsUnD1xHVb5EnqGXDgPWCttLUA2LhggbZJC6CkwtGPNYD5xGiQ1r5SUtt5O27mob5Oe-vZy2wMvmumd32QYi3ov7CWInc_ddg7cV4AzY-bIraCHVFZp4xNBB6NnWr7qExUgleRCKD771pS-HcvoaiJThNdhNsc6JikVW1Z9vINOPsH1lRSD_kFsO27lCRTu1L2VqUG4I1ZgVj8xyzqW6kh_jg", "refresh_token": "os.bl0BomrXS2OD4KQXLfvBkwJo3XEjj55ba_ecmJ9lVfp15aH4aEnJG0MJ", "expires_in": 7200, "sub": "Y0M8RSWsPDM_qMf6", "expires_at": "2022-11-28T00:09:48.398Z"}

token = credentials["token_type"] + " " + credentials["access_token"]

# url = str(input("Enter the url: "))
#url = "https://mypikpak.com/drive/all/VNE2WsquTKDwgZ2rSxM1Wn-lo1"

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")

service = Service("msedgedriver.exe")

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(login_url)
driver.execute_script(
    f"window.localStorage.setItem('credentials_YUMx5nI8ZU8Ap8pm', '{json.dumps(credentials)}');")
time.sleep(2)


def pikpakit(url, path):

    driver.get(url)
    time.sleep(3)

    captcha = driver.execute_script(
        "return JSON.parse(window.localStorage['captcha_YUMx5nI8ZU8Ap8pm']).token")

    id = driver.execute_script(
        "return window.localStorage.getItem('deviceid')")
    regex = r"\.(.*)xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    device_id = re.search(regex, id).group(1)
    time.sleep(5)

    files = driver.find_elements(By.CLASS_NAME, "row")
    ids = []
    urls = []
    for file in files:
        imgFile = file.find_element(
            By.XPATH, ".//div[1]/div/div")

        if imgFile.get_attribute("class") == 'folder-cover':
            id = file.get_attribute("id")
            nameFile = file.find_elements(
                By.XPATH, ".//div[2]/div")

            name = nameFile[1].get_attribute("textContent")
            url = [f"https://mypikpak.com/drive/all/{id}", f"\\{name}"]
            urls.append(url)

        else:
            ids.append(file.get_attribute("id"))

    reses = []
    for id in ids:
        res = requests.get(f"https://api-drive.mypikpak.com/drive/v1/files/{id}?usage=FETCH", headers={
            "authorization": token,
            "x-captcha-token": captcha,
            "x-device-id": device_id
        }).json()
        reses.append(res)
    if not (os.path.exists(path)):
        os.mkdir(path)
    for url in reses:
        if 'web_content_link' in url:
            urlo = url['web_content_link']
            wget.download(urlo, rf"{path}")

    for url in urls:
        pikpakit(url[0], rf"{path}{url[1]}")


pikpakit("https://mypikpak.com/drive/all/VNE2WzMUhcn-ZbirGNS913WHo1",
         "C:\\Users\\aarra\Downloads")
driver.close()
