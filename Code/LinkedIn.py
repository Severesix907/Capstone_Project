import requests
from bs4 import BeautifulSoup
import random
import pandas as pd

title = "Data Science"  # Job title
location = "United States"  # Job location
start = 0  # Starting point
pages = 1000 # Number of pages to scrape

# Initialize an empty list to store job information
job_list = []

for page in range(pages):
    list_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={title}&location={location}&start={start}"# Send a GET request to the URL and store the response
    response = requests.get(list_url)

    list_data = response.text
    list_soup = BeautifulSoup(list_data, "html.parser")
    page_jobs = list_soup.find_all("li") 
        
    id_list = []
    for job in page_jobs:
        base_card_div = job.find("div", {"class": "base-card"})
        if base_card_div is not None:
            job_id = base_card_div.get("data-entity-urn").split(":")[3]
            print(job_id)
            id_list.append(job_id)
        else:
            print("No element Found")
        

    # Loop through the list of job IDs and get each URL
    for job_id in id_list:
        # Construct the URL for each job using the job ID
        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        
        # Send a GET request to the job URL and parse the reponse
        job_response = requests.get(job_url)
        print(job_response.status_code)
        job_soup = BeautifulSoup(job_response.text, "html.parser")
        
        # Create a dictionary to store job details
        job_post = {}
        
        # Try to extract and store the job title
        try:
            job_post["job_title"] = job_soup.find("h2", {"class":"top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"}).text.strip()
        except:
            job_post["job_title"] = None
            
        # Try to extract and store the company name
        try:
            job_post["company_name"] = job_soup.find("a", {"class": "topcard__org-name-link topcard__flavor--black-link"}).text.strip()
        except:
            job_post["company_name"] = None
            
        # Try to extract and store the time posted
        try:
            job_post["time_posted"] = job_soup.find("span", {"class": "posted-time-ago__text topcard__flavor--metadata"}).text.strip()
        except:
            job_post["time_posted"] = None
            
        # Try to extract and store the number of applicants
        try:
            job_post["num_applicants"] = job_soup.find("span", {"class": "num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"}).text.strip()
        except:
            job_post["num_applicants"] = None
            # We are going to look for compansation 
        try:
            job_post["employment_type"] = job_soup.find("span", {"class": "description__job-criteria-text description__job-criteria-text--criteria"}).text.strip()
        except:
            job_post["employment_type"] = None
            #This one we are going to have to search for it since there is alot of data in the class
        try:
            job_post["salary"] = job_soup.find("div", {"class": "compensation__salary-range"}).text.strip()
        except:
            job_post["salary"] = None
            
        # Append the job details to the job_list
        job_list.append(job_post)
    start += 25

    # Create a DataFrame from the job_list
    job_list_df = pd.DataFrame(job_list)
    print(job_list)

    # Save the DataFrame to a CSV file
    job_list_df.to_csv("job_list.csv", index=False)
    
