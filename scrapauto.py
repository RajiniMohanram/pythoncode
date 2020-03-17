from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

prod_name=""
def scrape(key):
    base_url='https://www.amazon.com/'
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    DIR_PATH=os.getcwd()
    driver=webdriver.Chrome(DIR_PATH+'\chromedriver.exe')
    driver.get(base_url)
    
    driver.find_element_by_id('twotabsearchtextbox').clear()
    driver.find_element_by_id('twotabsearchtextbox').send_keys(key)
    driver.find_element_by_xpath("//input[@tabindex='20']").click()
    
    asin_links = driver.find_elements_by_xpath("//a[@class='a-link-normal a-text-normal']")
    #repeat
    driver.get(asin_links[0].get_attribute('href'))
    driver.find_element_by_xpath("//a[@data-hook='see-all-reviews-link-foot']").click()
    global prod_name
    prod_name=driver.find_element_by_xpath("//a[@data-hook='product-link']").get_attribute('innerHTML')
    rev_elems = driver.find_elements_by_xpath("//span[@data-hook='review-body']")
    #rev_elem = rev_elems[0].find_element_by_tag_name('span').get_attribute('innerHTML')
    print('----------- Product Name -------------------')
    print(prod_name)
    print('----------- Reviews ------------------------')
    reviews=[]
    for elem in rev_elems:
        reviews.append(elem.find_element_by_tag_name('span').get_attribute('innerHTML'))
    
    driver.close()
    return reviews