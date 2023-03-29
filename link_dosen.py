import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import collections
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.page_load_strategy = 'normal'
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('extensionLoadTimeout', 60000)
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--no-sandbox')
chrome_options.headless = True


NAME_FILE = "762_MUHAMMADIYAH_MANADO_link_prodi"
PATH = "chromedriver.exe"

links = []
def unlist(var):
    for i in var:
        return i
    
df = pd.read_csv(NAME_FILE + ".csv")
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
        
        wait = WebDriverWait(driver, 20)
        print("!! STEP")
        jabatan_fungsional = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/section/div/div[1]/div/div/table/tbody/tr[7]/td[3]')))
        # jabatan_fungsional = driver.find_elements(By.XPATH, '//*[@id="root"]/div/main/div/section/div/div[1]/div/div/table/tbody/tr[7]/td[3]')
        print(jabatan_fungsional.text)
        t.append(jabatan_fungsional.text)
        end = time.time()
        print(end-start)
        driver.quit()
    
    c = collections.Counter(t)
    new_col = [x for x in df_new.keys() if x not in c.keys()]
    new_col.remove("Prodi")
    new_col.remove("Jenjang")
    print(new_col)

    df_new["Prodi"].append(df["Prodi"][count])
    df_new["Jenjang"].append(df["Jenjang"][count])

    if len(new_col) != 0:
        for i in new_col:
            df_new[f"{i}"].append(0)
        for i in c.keys():
            if i not in df_new.keys():
                pass
            else:
                df_new[i].append(c[i])
    else:
        for i in c.keys():
            df_new[i].append(c[i])

    print(df_new)
    count += 1
    df_new_csv = pd.DataFrame(df_new)
    df_new_csv.to_csv(NAME_FILE + "_counted_" + ".csv", index=False)

    
