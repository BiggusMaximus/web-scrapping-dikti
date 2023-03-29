import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import collections

NAME_FILE = "ITB_link_prodi.csv"
PATH = "chromedriver.exe"
links = []
def unlist(var):
    for i in var:
        return i
    
df = pd.read_csv(NAME_FILE)
df_new = {
    "Prodi": [],
    "Jenjang": [],
    "Profesor": [],
    "Lektor Kepala": [],
    "Lektor": [],
    "Asisten Ahli": [],
    "-": []
}
count = 0
for i in df["Link"]:
    print(f"Link : {i} \n\n")
    driver = webdriver.Chrome(executable_path=PATH)
    driver.get(i)
    wait = WebDriverWait(driver, 5)
    print("! STEP")
    tbody = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="t01"]/tbody')))

    # tbody = driver.find_element(By.XPATH, '//*[@id="t01"]/tbody')
    for tr in tbody.find_elements(By.XPATH, '//tr'):
        link_dosen = unlist(tr.find_elements(By.XPATH, './/td[2]/a'))
        jabatan_fungsional = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section/div/div[1]/div/div/table/tbody/tr[7]/td[3]')
    
        if link_dosen != None:
            links.append(link_dosen.get_attribute('href'))
            print(link_dosen.get_attribute('href'))
    driver.close()

    t = []
    for j in links:
        start = time.time()
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(j)
        wait = WebDriverWait(driver, 5)
        print("!! STEP")
        jabatan_fungsional = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/section/div/div[1]/div/div/table/tbody/tr[7]/td[3]')))
        # jabatan_fungsional = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section/div/div[1]/div/div/table/tbody/tr[7]/td[3]')
        print(jabatan_fungsional.text)
        t.append(jabatan_fungsional.text)
        end = time.time()
        print(end-start)
    
    c = collections.Counter(t)
    new_col = [x for x in c.keys() if x not in df_new.keys()]
    print(new_col)

    for i in c.keys():
        if len(new_col) != 0:
            df_new[f"{unlist(new_col)}"] = [c[unlist(new_col)]]
        else:
            df_new[i].append(c[i])
 
    df_new["Prodi"].append(df["Prodi"][count])
    df_new["Jenjang"].append(df["Jenjang"][count])
    print(df_new)
    count += 1

df_new.to_csv("a.csv", index=False)
    