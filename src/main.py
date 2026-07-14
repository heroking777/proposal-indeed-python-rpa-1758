# Dependencies:
# pip install selenium pandas

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def setup_driver():
    # Set up Chrome WebDriver
    service = Service('path/to/chromedriver')  # Update with the path to your chromedriver executable
    driver = webdriver.Chrome(service=service)
    return driver

def login_to_indeed(driver, username, password):
    # Navigate to Indeed login page
    driver.get('https://www.indeed.com/account/login')
    
    # Wait for the login form to load and enter credentials
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-email')))
    driver.find_element(By.ID, 'login-email').send_keys(username)
    driver.find_element(By.ID, 'login-password').send_keys(password)
    
    # Submit the login form
    driver.find_element(By.ID, 'login-submit').click()
    
    # Wait for the dashboard to load after login
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'indeed-dashboard')))

def get_job_listings(driver):
    # Navigate to job listings page
    driver.get('https://www.indeed.com/jobs')
    
    # Wait for the job list to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'jobsearch-SerpJobCard')))
    
    # Extract job titles and URLs
    jobs = []
    job_elements = driver.find_elements(By.CLASS_NAME, 'jobsearch-SerpJobCard')
    for job in job_elements:
        title = job.find_element(By.TAG_NAME, 'h2').text.strip()
        url = job.find_element(By.TAG_NAME, 'a')['href']
        jobs.append({'title': title, 'url': url})
    
    return jobs

def delete_jobs(driver, jobs_to_delete):
    # Navigate to each job listing and delete if conditions are met
    deleted_jobs = []
    for job in jobs_to_delete:
        driver.get(job['url'])
        
        # Wait for the job details page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'jobsearch-JobInfoHeader-title')))
        
        # Check if the job meets deletion criteria (e.g., status is '休止中')
        status = driver.find_element(By.XPATH, '//div[contains(@class, "jobsearch-CompanyReview--status")]').text.strip()
        if status == '休止中':
            # Delete the job
            delete_button = driver.find_element(By.XPATH, '//button[contains(text(), "Delete") or contains(text(), "非公開にする")]')
            delete_button.click()
            
            # Confirm deletion
            confirm_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Confirm")]')))
            confirm_button.click()
            
            deleted_jobs.append(job['title'])
    
    return deleted_jobs

def save_log(deleted_jobs):
    # Save the list of deleted jobs to a CSV file
    df = pd.DataFrame(deleted_jobs, columns=['Deleted Job Title'])
    df.to_csv('deleted_jobs.csv', index=False)
    print("Log saved to 'deleted_jobs.csv'")

def main():
    username = 'your_indeed_username'
    password = 'your_indeed_password'
    
    driver = setup_driver()
    login_to_indeed(driver, username, password)
    
    jobs = get_job_listings(driver)
    
    # Example criteria for deletion: jobs older than 30 days and status is '休止中'
    current_time = time.time()
    deleted_jobs = []
    for job in jobs:
        job_details_page = job['url']
        driver.get(job_details_page)
        
        # Wait for the job details page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'jobsearch-JobInfoHeader-title')))
        
        # Extract job status and last updated time
        status = driver.find_element(By.XPATH, '//div[contains(@class, "jobsearch-CompanyReview--status")]').text.strip()
        last_updated_text = driver.find_element(By.XPATH, '//span[contains(text(), "Updated")]').text.strip()
        last_updated_time = pd.to_datetime(last_updated_text.split(': ')[1], format='%b %d, %Y')
        
        if status == '休止中' and (current_time - last_updated_time.timestamp()) > 30 * 24 * 60 * 60:
            deleted_jobs.append(job['title'])
    
    deleted_jobs = delete_jobs(driver, jobs_to_delete=deleted_jobs)
    save_log(deleted_jobs)
    
    driver.quit()

if __name__ == "__main__":
    main()
```

This script automates the process of logging into Indeed, retrieving job listings, and deleting jobs based on specified criteria. It uses Selenium for web automation and pandas for saving logs to a CSV file. Make sure to update the `path/to/chromedriver` with the actual path to your ChromeDriver executable and provide valid login credentials for Indeed.