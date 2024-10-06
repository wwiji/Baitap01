from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re


#Tao dataframe rong~
data = pd.DataFrame({'name the band ': [], 'year active ': []})
#Khoi tao danh sách các đường link
href_list = []

#url
url = "https://en.wikipedia.org/wiki/List_of_musicians"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)

ul_tag = driver.find_elements(By.XPATH, "//div[@class='div-col']")
ul_name = ul_tag[:19]

for ul in ul_name:
    li = ul.find_elements(By.TAG_NAME, "li")
    for i in li:
        a = i.find_element(By.TAG_NAME, "a")
        href_list.append(a.get_attribute("href"))

#hien thi so luong cac duong link lay được
print(len(href_list))

#Hien thi duong link cuối lấy được
print(href_list[-1])

# Khơi tạo list lưu trữ link các nhóm nhạc
href_list_band = []

# Duyệt qua từng link
for href in href_list:
    driver.get(href)
    time.sleep(2)
    # Lấy các đường link thẻ li trong thẻ div có class = "div-col"
    ul_tag = driver.find_elements(By.XPATH, "//div[@class='div-col']/ul/li")
    # them vao list cac duong link nhom nhac
    for ul in ul_tag:
        try:
            a_tag = ul.find_element(By.TAG_NAME, "a")
            href = a_tag.get_attribute("href")
            href_list_band.append(href)
        except:
            print("error")

print(len(href_list_band))

conti = 1
for href in href_list_band:
    driver.get(href)
    time.sleep(2)

    # Lấy tên nhóm nhạc
    try:
        name = driver.find_element(By.TAG_NAME, "h1").text
    except:
        name = ""

    # Lấy năm hoạt động
    # Active years nằm trong thẻ th hoặc thẻ div
    try:
        tables = driver.find_elements(By.XPATH, "//table[@class='infobox vcard plainlist']/tbody/tr/th")
        for table in tables:
            # Nếu tìm thấy thẻ th chứa text "Years active" thì lấy thẻ td kế tiếp
            if table.text == "Years active":
                try:
                    year_active = table.find_element(By.XPATH, "following-sibling::td").text
                    break
                except:
                    year_active = ""
            # Nếu không tìm thấy thẻ th chứa text "Years active" thì tìm thẻ div chứa class = "hlist"
            else:
                try:
                    year_active = " "
                    div = table.find_element(By.XPATH, "//div[@class='hlist']")
                    li = div.find_elements(By.TAG_NAME, "li")
                    for l in li:
                        if "Years active" in l.text:
                            year_active = l.text + ", "
                            break
                        else:
                            year_active = ""
                except:
                    year_active = ""
    except:
        year_active = " "

    # Lưu dữ liệu vào dataframe
    save = pd.DataFrame({'name the band ': [name], 'year active ': [year_active]})
    data = pd.concat([data, save], ignore_index=True)
    conti += 1
    if conti % 500 == 0:
        print(conti)
        files = str(conti) + ".xlsx"
        data.to_excel(files, index=False)

# Lưu dữ liệu vào file excel
data.to_excel("musician.xlsx", index=False)
driver.quit()