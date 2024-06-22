import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
PATH = "./chromedriver.exe"
service = Service(PATH)
driver = webdriver.Chrome(service=service)
driver.get("https://www.indeed.com")

# Search Parameters
query = "Software Engineer New Grad"
location = "United States"
stop_on_page = 8
age = 4

job_titles = []
employers = []
scraped_apply_urls = []
scraped_job_locations = []
scraped_ratings = []

page = 0

for i in range(int(stop_on_page)):
    url = f"https://www.indeed.com/jobs?q={query}&l={location}&start={page}&fromage={age}"
    driver.get(url)
    
    wait = WebDriverWait(driver, 10)
    jobs_div = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'jobsearch-SerpJobCard')))
    
    for job_element in jobs_div:
        job_title_element = job_element.find_element(By.CSS_SELECTOR, 'h2.title a')
        job_title = job_title_element.get_attribute('title')
        job_titles.append(job_title)
        
        job_id = job_element.get_attribute('data-jk')
        apply_url = "https://www.indeed.com/viewjob?jk=" + job_id
        scraped_apply_urls.append(apply_url)
        
        company_element = job_element.find_element(By.CSS_SELECTOR, 'span.company')
        company = company_element.text.strip() if company_element else None
        employers.append(company)
        
        location_element = job_element.find_element(By.CSS_SELECTOR, 'div.location.accessible-contrast-color-location')
        location = location_element.text.strip() if location_element else None
        scraped_job_locations.append(location)
        
        rating_element = job_element.find_element(By.CSS_SELECTOR, 'span.ratingsContent')
        rating = float(rating_element.text.strip().replace(',', '.')) if rating_element else None
        scraped_ratings.append(rating)
    
    page += 10
    time.sleep(random.uniform(1, 3))  # Sleep to mimic human behavior

# Ensure all lists are of the same length
while len(employers) != len(job_titles):
    employers.append("NaN")

job_data = pd.DataFrame({
    'Company': employers,
    'Post': job_titles,
    'Location': scraped_job_locations,
    'Link': scraped_apply_urls,
    'Rating': scraped_ratings
})

job_data.to_csv('Indeed_jobs.csv', index=False)

# Close the WebDriver
driver.quit()
 