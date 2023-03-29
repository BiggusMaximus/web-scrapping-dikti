from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
URL = "https://pddikti.kemdikbud.go.id/data_pt/Q0JCODYzMjQtQzU5OS00MzE0LUFDQjAtMjRFMzg3RjIxRkY0"
NAME = "762_MUHAMMADIYAH_MANADO"

df = {
    "Prodi" : [],
    "Jenjang" : [],
    "Status" : [],
    "Link" : [],
}

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(URL)
wait = WebDriverWait(driver, 20)
print("!! STEP")
tbody = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="t01"]/tbody')))

data = []
for tr in tbody.find_elements(By.XPATH, '//tr'):
    jenjang = tr.find_elements(By.XPATH, './/td[5]')
    status = tr.find_elements(By.XPATH, './/td[4]')
    
    if len(status) != 0:
        status = unlist(status).text
        jenjang = unlist(jenjang).text
        
        if evaluate(jenjang, status):
            prodi = tr.find_elements(By.XPATH, './/td[3]')
            prodi = unlist(prodi).text
            link_prodi = unlist(tr.find_elements(By.XPATH, './/td[3]/a')).get_attribute('href')


            # print(f"{jenjang}, {status}, {link_prodi}")
            df["Jenjang"].append(jenjang)
            df["Status"].append(status)
            df["Prodi"].append(prodi)
            df["Link"].append(link_prodi)
            t = pd.DataFrame(df)
            t.to_csv(f"{NAME}_link_prodi.csv", index=False)
driver.quit()
