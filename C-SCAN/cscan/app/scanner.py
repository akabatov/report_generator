from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from django.conf import settings

#Set the path for the driver and XPATHs for elements on a webpage 
PATH = settings.BASE_DIR + '/' + 'chromedriver.exe'
INPUT_XPATH = '//*[@id="panel"]/div[1]/input'
TEST_XPATH = '//body/div[3]/div[4]/div[1]/div[2]/div[4]'

#Class to create the 2 dimentional list and store information about containers 
class Scan():
    global file_length 

    def __init__(self, file, info_arr):
        self.file = file
        self.info_arr = info_arr


    #Function returns the path to the file that was uploaded by user
    def getPath(self):
        return settings.MEDIA_ROOT + "/" + self.file
    
    #Getter funtion for self.file
    def getFile_Name(self):
        return self.file

    #Function returns the global variable file_length 
    #Input  --- NONE
    #Output --- integer (file_length)
    def getFile_length(self):
        global file_length
        return file_length

    #Function gets rid of the commas and brackets and returns the 2D list
    # Input  --- NONE
    # Output --- list (2 dimentional list with container information)
    def getInfo_arr(self):
        result = (', '.join(l) for l in self.info_arr)
        return result

    #Function sets the length of the 2D list to specified values
    #Input  --- columns (amount of columns), rows (amount of rows)
    #Output --- NONE
    def setLength(self, columns, rows):
        self.info_arr = [[0 for x in range(columns)] for x in range(rows)]

    #Function puts a specified value into specified position of the 2D list
    #Input  --- row (y position), column (x position), value (value to input)
    #Output --- NONE
    def setInfo_arr(self, row, column, value):
        self.info_arr[row][column] = value

    
    #Function reads gets the file, reads all the info and stores it in a list
    #Input  --- NONE
    #Output --- List 
    def read_file(self):
        global file_length
        container_list = []
        path = self.getPath()
        with open(path, 'r') as f:
            line = f.readline()
            while  len(line) > 1:
                container_list.append(line.rstrip('\n'))
                line = f.readline()
        file_length = len(container_list)
        self.setLength(6, file_length)
        return container_list 


    #With each iteration function opens the browser, inputs the container ID, retrieves the information and stores it inside the 2 dimentional list
    #Input  --- NONE
    #Output --- NONE
    def scan_iteration(self):
        #Locate the WebDriver and open the webpage 
        driver = webdriver.Chrome(PATH)
        driver.get('https://sirius.searates.com/tracking/multitracking?')
        
        #List of container ids from uploaded file
        container_list = self.read_file()

        #Contianer index for 2D list
        container_number = 0

        #for each id in the uploaded file 
        for id in container_list:

            #Locate the input field, input ID and press ENTER
            search = driver.find_element(By.NAME, "container")
            search.send_keys(id)
            search.send_keys(Keys.RETURN)

            #element loaded and data is available 
            try:
                #Wait for 10 seconds if element loads
                wait = WebDriverWait(driver, 10, poll_frequency=1)
                element = wait.until_not(EC.presence_of_element_located((By.XPATH, TEST_XPATH)))

                #Retrieve HTML of the page 
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                #Find requiered information and store it in the list 
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

                #clear the search bar
                search.clear()

            #Element didn't load or no data available
            except:
                #fill the list with 'NA'
                self.setInfo_arr(container_number, 0, id)
                self.setInfo_arr(container_number, 1, "NA")
                self.setInfo_arr(container_number, 2, "NA")
                self.setInfo_arr(container_number, 3, "NA")
                self.setInfo_arr(container_number, 4, "NA")
                self.setInfo_arr(container_number, 5, "NA")

                #clear the search bar
                search.clear()

            #increment the y index in 2D array
            container_number += 1
    


