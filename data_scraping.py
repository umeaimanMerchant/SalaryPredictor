# -*- coding: utf-8 -*-
"""
@author: UMEAIMAN
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
import pandas as pd
import time
from selenium.webdriver.common.by import By


def fetch_jobs(keyword, num_pages):
    #options = Options()
    #options.add_argument("window-size=1920,1080")
    #Enter your chromedriver.exe path below
    #chrome_path = r"C:\Users\AIMAN\data science learn\Glassdoor-Scraper-Final-main\chromedriver.exe"
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    #driver = webdriver.Chrome(executable_path=chrome_path, options=options)
    driver.get("https://www.glassdoor.com/Job/Home/recentActivity.htm")
    search_input = driver.find_element(By.ID, "sc.keyword")
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.ENTER)
    time.sleep(2)
    
    
    
    
    company_name = []
    job_title = []
    salary_est = []
    location = []
    job_description = []
    salary_estimate = []
    company_size = []
    company_type = []
    company_sector = []
    company_industry = []
    company_founded = []
    company_revenue = []
    
    
    
    #Set current page to 1
    current_page = 1     
        
        
    #time.sleep(3)
    
    while current_page <= num_pages:   
        
        done = False
        while not done:
            job_cards = driver.find_elements(By.XPATH, "//article[@id='MainCol']//ul/li[@data-adv-type='GENERAL']")
            for card in job_cards:
                card.click()
                time.sleep(1)

                #Closes the signup prompt- /html/body/div[12]/div/div/div/div[2]/button
                try:
                    driver.find_element(By.XPATH,".//span[@class='SVGInline modal_closeIcon']").click()
                    driver.find_element(By.XPATH,"/html/body/div[12]/div/div/div/div[2]/button").click()
                    print("close")
                    time.sleep(2)
                except NoSuchElementException:
                    time.sleep(2)
                    print("Not close")
                    pass

                #Expands the Description section by clicking on Show More- //div[@class='css-t3xrds e856ufb2']
                try:
                    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/div/div/div[2]/section/div/div/article/div/div[2]/div[1]/div[1]/div/div[2]").click()
                    time.sleep(1)
                except NoSuchElementException:
                    card.click()
                    print(str(current_page) + '#ERROR: no such element')
                    time.sleep(30)
                    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/div/div/div[2]/section/div/div/article/div/div[2]/div[1]/div[1]/div/div[2]").click()
                except ElementNotInteractableException:
                    card.click()
                    driver.implicitly_wait(30)
                    print(str(current_page) + '#ERROR: not interactable')
                    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div/div[2]/section/div/div/article/div/div[2]/div[1]/div[1]/div/div[2]").click()

                #Scrape 
                #//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]/div
                #
                try:
                    company_name.append(driver.find_element(By.XPATH,'//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]/div').text)
                    print(driver.find_element(By.XPATH,'//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]/div').text)
                except Exception as e: 
                    print(e)
                    #pass

                try:
                    job_title.append(driver.find_element(By.XPATH,'//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[2]').text)
                    print(driver.find_element(By.XPATH,'//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[2]').text)
                except:
                    job_title.append("#N/A")
                    print("No value- title")
                    pass

                try:
                    location.append(driver.find_element(By.XPATH, '//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[3]').text)
                    print(driver.find_element(By.XPATH, '//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[3]').text)
                except:
                    location.append("#N/A")
                    pass

                try:
                    job_description.append(driver.find_element(By.XPATH, './/div[@class="jobDescriptionContent desc"]').text)
                    print(driver.find_element(By.XPATH, './/div[@class="jobDescriptionContent desc"]').text)
                except Exception as e: 
                    print(e)
                    job_description.append("#N/A")

                try:
                    salary_estimate.append(driver.find_element(By.XPATH, '//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[4]/span').text)
                    print(driver.find_element(By.XPATH, '//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[4]/span').text)
                except:
                    salary_estimate.append("#N/A")
                    pass
                
                try:
                    company_size.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Size']//following-sibling::*").text)
                except:
                    company_size.append("#N/A")
                    pass
                
                try:
                    company_type.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Type']//following-sibling::*").text)
                except:
                    company_type.append("#N/A")
                    pass
                    
                    #//*[@id="JobDesc1008847978894"]/div/p[11]
                try:
                    company_sector.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Sector']//following-sibling::*").text)
                except:
                    company_sector.append("#N/A")
                    pass
                    
                try:
                    company_industry.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Industry']//following-sibling::*").text)
                except:
                    company_industry.append("#N/A")
                    pass
                    
                try:
                    company_founded.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Founded']//following-sibling::*").text)
                except:
                    company_founded.append("#N/A")
                    pass
                    
                try:
                    company_revenue.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Revenue']//following-sibling::*").text)
                except:
                    company_revenue.append("#N/A")
                    pass
                    
                    
                    
                    
                done = True
                
       # Moves to the next page         
        if done:
            print(str(current_page) + ' ' + 'out of' +' '+ str(num_pages) + ' ' + 'pages done')
        #    driver.find_element(By.XPATH, "//span[@alt='next-icon']").click()   
            current_page = current_page + 1
        #    time.sleep(4)
            




    driver.close()
    df = pd.DataFrame({'company': company_name, 
    'job title': job_title,
    'location': location,
    'job description': job_description,
    'salary estimate': salary_estimate,
    'company_size': company_size,
    'company_type': company_type,
    'company_sector': company_sector,
    'company_industry' : company_industry, 'company_founded' : company_founded, 'company_revenue': company_revenue})
    
    df.to_csv(keyword + '.csv')
                       
fetch_jobs("Data Scientist", 1)
