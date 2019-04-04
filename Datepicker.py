from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import datetime

def SelectDate(driver, InputBox, Year, Month, Day):
    currentDateTime = datetime.datetime.today()

    currentMonthAndYear = (currentDateTime.strftime("%B" + " " + "%Y"))
    currentMonthAbr = currentDateTime.strftime("%b")
    currentYear = currentDateTime.strftime("%Y")
    currentDayDate = (currentDateTime.strftime("%d").lstrip("0"))

    driver.implicitly_wait(5)

    # Click to open drop-down
    driver.find_element_by_xpath("//input[contains(@class,'input-sm form-control "+InputBox +"')]").click()

    # Open Month Select
    driver.find_element_by_xpath("//th[@colspan='5'][contains(.,'" +currentMonthAndYear +"')]").click()
    #Open Year Select
    driver.find_element_by_xpath("(//th[@colspan='5'][contains(.,'" +currentYear +"')])[2]").click()
    # Select Year
    driver.find_element_by_xpath("//span[@class='year'][contains(.,'"+Year +"')]").click()
    # Select Month
    driver.find_element_by_xpath("//span[@class='month'][contains(.,'"+Month +"')]").click()
    # Select Day
    if Day == currentDayDate:
        driver.find_element_by_xpath("//td[@class='today day'][contains(.,'" + Day + "')]").click()
    elif Day != currentDayDate:
        driver.find_element_by_xpath("//td[@class='day'][contains(.,'" +Day +"')]").click()

'''
driver = webdriver.Chrome()
driver.get("https://twitter.com/search-advanced?lang=en")
driver.implicitly_wait(5)
SelectDate(driver=driver, InputBox="input-since", Year="2017", Month="Dec", Day="3")
SelectDate(driver=driver, InputBox="input-until", Year="2018", Month="Jul", Day="9")
driver.close()
'''