from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time

PATH = r"C:\Program Files (x86)\chromedriver-win64\chromedriver.exe"

def naukri(job_title, location, experience):
    service = Service(PATH)
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.naukri.com/")
    print("Opened Naukri.com")

    wait = WebDriverWait(driver, 3)
    try:
        job_title_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter skills / designations / companies"]')))
        location_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter location"]')))
        experience_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'expereinceDD')))
        print("Found search input fields")
    except TimeoutException:
        print("Search input fields took too long to load!")
        driver.quit()
        return []

    # Enter the job title, location, and experience and submit
    job_title_input.send_keys(job_title)
    location_input.send_keys(location)
    
    # Click the experience dropdown to open it
    experience_dropdown.click()

    # Locate the experience option using XPath with the desired experience text
    experience_option_xpath = f'//ul[contains(@class, "dropdown")]//span[text()="{experience}"]'
    try:
        experience_option = wait.until(EC.element_to_be_clickable((By.XPATH, experience_option_xpath)))
        experience_option.click()
        print(f"Selected experience: {experience}")
    except TimeoutException:
        print(f"Timeout selecting experience: {experience}")
        driver.quit()
        return []

    job_title_input.send_keys(Keys.RETURN)
    print("Submitted search query")

    pages_to_scrape = 3
    current_page = 1
    jobs = []
    # Wait for the results page to load and check for job listing elements
    while current_page<=pages_to_scrape:
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.srp-jobtuple-wrapper')))
            print("Found job listing elements")
        except TimeoutException:
            print("Job listings took too long to load!")
            driver.quit()
            return []

        job_elements = driver.find_elements(By.CSS_SELECTOR, 'div.srp-jobtuple-wrapper')

        for job_element in job_elements:
            job = {}
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, 'a.title')
                job['link'] = title_element.get_attribute('href')
                job['title'] = title_element.text
            except NoSuchElementException:
                job['title'] = "Title not found"

            try:
                company_element = job_element.find_element(By.CSS_SELECTOR, 'a.comp-name')
                job['company'] = company_element.text
            except NoSuchElementException:
                job['company'] = "Company not found"

            try:
                location_element = job_element.find_element(By.CSS_SELECTOR, 'span.locWdth')
                job['location'] = location_element.text
            except NoSuchElementException:
                job['location'] = "Location not found"

            try:
                experience_element = job_element.find_element(By.CSS_SELECTOR, 'span.expwdth')
                job['experience'] = experience_element.text
            except NoSuchElementException:
                job['experience'] = "Experience not found"

            try:
                salary_element = job_element.find_element(By.CSS_SELECTOR, 'span.sal')
                job['salary'] = salary_element.text
            except NoSuchElementException:
                job['salary'] = "Salary not found"

            try:
                tags_elements = job_element.find_elements(By.CSS_SELECTOR, 'div.row5 ul.tags-gt li.tag-li')
                tags = [tag_element.text for tag_element in tags_elements] if tags_elements else []
                job['tags'] = tags
            except NoSuchElementException:
                job['tags'] = []

            jobs.append(job)
        
        current_page+=1
        if current_page<=pages_to_scrape:
            try:
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="styles_btn-secondary__2AsIP"]')))
                next_button.click()
                time.sleep(0.5)
                print(f"Navigating to page {current_page}")
            except:
                print("Next button not found, exiting")
                break

    # Close the WebDriver
    driver.quit()

    return jobs

if __name__ == "__main__":
    # User input
    job_title = 'Data Science'
    location = 'Delhi'
    experience = '15 years'
    start_time = time.time()
    job_listings = naukri(job_title, location, experience)
    end_time = time.time()
    print("Total Runtime:", end_time - start_time)
    print("Total Jobs Found:", len(job_listings))

    # print(pd.DataFrame(job_listings))