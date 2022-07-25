from importlib.resources import path
from tracemalloc import start
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from django.conf import settings


PATH = r'C:\Users\alexander.kabatov\OneDrive - Gestion Vamcorp Ltee\Desktop\C-SCAN\chromedriver.exe'
INPUT_XPATH = '//*[@id="panel"]/div[1]/input'
TEST_XPATH = '//body/div[3]/div[4]/div[1]/div[2]/div[4]'

class Scan():
    global file_length 

    def __init__(self, file, info_arr):
        self.file = file
        self.info_arr = info_arr

    def getPath(self):
        return settings.MEDIA_ROOT + "/" + self.file
    
    def getFile_Name(self):
        return self.file

    def getFile_length(self):
        global file_length
        return file_length
        
    def getInfo_arr(self):
        result = (', '.join(l) for l in self.info_arr)
        return result

    def setLength(self, columns, rows):
        self.info_arr = [[0 for x in range(columns)] for x in range(rows)]

    def setInfo_arr(self, object, pos, value):
        self.info_arr[object][pos] = value
    
    def read_file(self):
        global file_length
        container_list = []
        path = self.getPath()
        print(self.getPath())
        with open(path, 'r') as f:
            line = f.readline()
            while  len(line) > 1:
                container_list.append(line.rstrip('\n'))
                line = f.readline()
        file_length = len(container_list)
        self.setLength(6, file_length)
        return container_list 

    def scan_iteration(self):

        driver = webdriver.Chrome(PATH)
        driver.get('https://sirius.searates.com/tracking/multitracking?')
        
        container_list = self.read_file()
        container_number = 0

        for id in container_list:
            search = driver.find_element(By.NAME, "container")
            search.send_keys(id)
            search.send_keys(Keys.RETURN)

            try:
                wait = WebDriverWait(driver, 10, poll_frequency=1)
                element = wait.until_not(EC.presence_of_element_located((By.XPATH, TEST_XPATH)))

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                sealine = soup.find('p', {'class': 'container-id'}).get('data-sealine')
                destination_info = soup.find('div', {'class': 'destination'})
                children = destination_info.findChildren('div', recursive=False)
                start_date = soup.find('div', {'class': 'bl-start-date eta'}).text
                end_date = soup.find('div', {'class': 'bl-finish-date etd'}).text
                self.setInfo_arr(container_number, 0, id)
                self.setInfo_arr(container_number, 1, sealine)
                self.setInfo_arr(container_number, 2, children[0].text)
                self.setInfo_arr(container_number, 3, children[1].text)
                self.setInfo_arr(container_number, 4, start_date)
                self.setInfo_arr(container_number, 5, end_date)

                # container_info.append(id)
                # container_info.append(soup.find('p', {'class': 'container-id'}).get('data-sealine'))
                # destination_info = soup.find('div', {'class': 'destination'})
                # children = destination_info.findChildren('div', recursive=False)
                # container_info.append(children[0].text)
                # container_info.append(children[1].text)
                # container_info.append(soup.find('div', {'class': 'bl-start-date eta'}).text)
                # container_info.append(soup.find('div', {'class': 'bl-finish-date etd'}).text)

                search.clear()

            except:
                self.setInfo_arr(container_number, 0, id)
                self.setInfo_arr(container_number, 1, "NA")
                self.setInfo_arr(container_number, 2, "NA")
                self.setInfo_arr(container_number, 3, "NA")
                self.setInfo_arr(container_number, 4, "NA")
                self.setInfo_arr(container_number, 5, "NA")
                # container_info.append(id)
                # i = 0
                # while i < 6:
                #     container_info.append('NA')
                #     i+=1
                search.clear()
            
            container_number += 1
    


