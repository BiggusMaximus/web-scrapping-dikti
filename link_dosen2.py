import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support import expected_conditions as EC
import collections

NAME_FILE = "ITB_link_prodi.csv"
PATH = "/chromedriver.exe"
URL = "https://pddikti.kemdikbud.go.id/data_prodi/QjQ5MzIxOEYtNzJCRi00NjBCLTk2NzctQzcxNDhDM0U3Mzkw/20221"

def unlist(var):
    for i in var:
        return i
    
df = pd.read_csv(NAME_FILE)

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(URL)
wait = WebDriverWait(driver, 3)
tbody = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="t01"]/tbody')))

links = []

for tr in tbody.find_elements(By.XPATH, '//tr'):
    link_dosen = unlist(tr.find_elements(By.XPATH, './/td[2]/a'))
    if link_dosen != None:
        links.append(link_dosen.get_attribute('href'))
        print(link_dosen.get_attribute('href'))
driver.close()

count = 0
t = []
for i in links:
    start = time.time()
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(i)
    jabatan_fungsional = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section/div/div[1]/div/div/table/tbody/tr[7]/td[3]')
    # wait = WebDriverWait(driver, 10)
    # jabatan_fungsional = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/section/div/div[1]/div/div/table/tbody/tr[7]/td[3]')))
    print(unlist(jabatan_fungsional).text)
    t.append(unlist(jabatan_fungsional).text)
    end = time.time()
    print(end-start)

c = collections.Counter(t)
print(c.items())
driver.close()