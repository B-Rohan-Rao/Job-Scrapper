import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time

start_time = time()

# Initialize WebDriver
driver = webdriver.Chrome()

# Search Parameters
no_of_jobs = 5
keyword = "Software Engineer"
location = "Delhi, India"

job_id = []
post_title = []
company_name = []
post_date = []
job_location = []

i = 0
while i < (no_of_jobs / 25):
    i += 1
    url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}&start={i*25}"
    driver.get(url)
    sleep(3)
    
    wait = WebDriverWait(driver, 10)
    job_container = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.jobs-search__results-list li')))
    
    print(f'You are scraping information about {len(job_container)} jobs from page {i}')

    for job_element in job_container:
        try:
            job_title = job_element.find_element(By.CSS_SELECTOR, 'h3.base-search-card__title').text.strip()
            post_title.append(job_title)
        except Exception as e:
            print(f"Error occurred while fetching job title: {e}")
            post_title.append("N/A")
        
        try:
            job_link = job_element.find_element(By.CSS_SELECTOR, 'a.base-card__full-link').get_attribute('href')
            job_id.append(job_link)
        except Exception as e:
            print(f"Error occurred while fetching job link: {e}")
            job_id.append("N/A")
        
        try:
            company = job_element.find_element(By.CSS_SELECTOR, 'h4.base-search-card__subtitle').text.strip()
            company_name.append(company)
        except Exception as e:
            print(f"Error occurred while fetching company name: {e}")
            company_name.append("N/A")
        
        try:
            location = job_element.find_element(By.CSS_SELECTOR, 'span.job-search-card__location').text.strip()
            job_location.append(location)
        except Exception as e:
            print(f"Error occurred while fetching location: {e}")
            job_location.append("N/A")
        
        try:
            post_date_element = job_element.find_element(By.CSS_SELECTOR, 'time')
            post_date.append(post_date_element.get_attribute('datetime'))
        except Exception as e:
            print(f"Error occurred while fetching post date: {e}")
            post_date.append("N/A")
    
    sleep(3)  # Adjust sleep to prevent being flagged as a bot

# Ensure all lists are of the same length
while len(company_name) != len(post_title):
    company_name.append("N/A")

job_data = pd.DataFrame({
    'Date': post_date,
    'Company': company_name,
    'Post': post_title,
    'Location': job_location,
    'Link': job_id
})

job_data.to_csv('LinkedIn_jobs.csv', index=False)

# Close the WebDriver
driver.quit()

print("Scraping completed. Total time:", time() - start_time)
