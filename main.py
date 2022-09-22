from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import openpyxl

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--disable-setuid-sandbox")
chromeOptions.add_argument("--remote-debugging-port=9222")
chromeOptions.add_argument("--disable-dev-shm-using")
chromeOptions.add_argument("--disable-extensions")
chromeOptions.add_argument("--disable-gpu")
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("disable-infobars")
chromeOptions.add_argument(r"user-data-dir=.\cookies\\test")

company_names = pd.read_excel('C:/Users/C88038/IdeaProjects/linkedin_scraper/Company_names_extended.xlsx')
company_names_list = company_names['company_name'].values.tolist()
companies_with_bios = {}
for i in company_names_list:
    driver = webdriver.Chrome('C:/Users/C88038/IdeaProjects/linkedin_scraper/chromedriver.exe', chrome_options=chromeOptions)
    driver.get('https:www.google.com')
    sleep(1)

    search_query = driver.find_element(By.NAME,"q")
    search_query.send_keys(f'site:linkedin.com/company/ AND "{i}"')
    sleep(1)

    search_query.send_keys(Keys.RETURN)
    sleep(3)

    results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
    if len(results)>0:
        url_unformatted = results[0].find_element(By.TAG_NAME, "a")
        linkedin_url = url_unformatted.get_attribute("href")
        driver.get(linkedin_url)
        sleep(1)
        companies_with_bios.update({i:driver.find_element(By.CLASS_NAME,"about-us__description").text.strip()})
        print(driver.find_element(By.CLASS_NAME,"about-us__description").text.strip())
    else:
        companies_with_bios.update({i:'no company information found on Linkedin'})

    df = pd.DataFrame(data=companies_with_bios, index=[0])
    df = df.T
    df.to_excel('C:/Users/C88038/IdeaProjects/linkedin_scraper/company_names_with_bios2.xlsx')
    driver.quit()
    sleep(3)
