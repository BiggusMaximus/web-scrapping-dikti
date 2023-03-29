from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

def unlist(var):
    for i in var:
        return i

def evaluate(jenjang, status):
    if status == "Aktif":
        if jenjang == "S1":
            return True
        elif jenjang == "S2":
            return True
        elif jenjang == "S3":
            return True
            

PATH = "/chromedriver.exe"
URL = "https://pddikti.kemdikbud.go.id/data_pt/QTFFOEMzNTYtNDhFRi00ODcxLUFGM0UtODUwNzk0NDNGOTUy"
NAME = "ITB"

df = {
    "Prodi" : [],
    "Jenjang" : [],
    "Status" : [],
    "Link" : [],
}

driver = webdriver.Chrome(executable_path=PATH)
driver.get(URL)

tbody = driver.find_element(By.XPATH, '//*[@id="t01"]/tbody')

data = []
for tr in tbody.find_elements(By.XPATH, '//tr'):
    jenjang = tr.find_elements(By.XPATH, './/td[5]')
    status = tr.find_elements(By.XPATH, './/td[4]')
    
    if len(status) != 0:
        status = unlist(status).text
        jenjang = unlist(jenjang).text
        
        if evaluate(jenjang, status):
            link_prodi = unlist(tr.find_elements(By.XPATH, './/td[3]/a')).get_attribute('href')
            prodi = tr.find_elements(By.XPATH, './/td[3]')
            prodi = unlist(prodi).text

            # print(f"{jenjang}, {status}, {link_prodi}")

            df["Jenjang"].append(jenjang)
            df["Status"].append(status)
            df["Prodi"].append(prodi)
            df["Link"].append(link_prodi)

            t = pd.DataFrame(df)
            t.to_csv(f"{NAME}_link_prodi.csv", index=False)
driver.quit()
