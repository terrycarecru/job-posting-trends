import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def scrape_job_posts(job_title, location):
    url = f"https://www.indeed.com/jobs?q={job_title}&l={location}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    job_elems = soup.find_all('div', class_='jobsearch-SerpJobCard')
    job_data = []

    for job_elem in job_elems:
        title_elem = job_elem.find('h2', class_='title')
        company_elem = job_elem.find('span', class_='company')
        location_elem = job_elem.find('div', class_='location')
        date_elem = job_elem.find('span', class_='date')

        if None in (title_elem, company_elem, location_elem, date_elem):
            continue

        job_data.append({
            'title': title_elem.text.strip(),
            'company': company_elem.text.strip(),
            'location': location_elem.text.strip(),
            'date_posted': date_elem.text.strip(),
            'scraped_date': datetime.datetime.now().strftime('%Y-%m-%d')
        })

    return job_data

# Example use
job_posts = scrape_job_posts("UX Designer", "San Francisco, CA")
df = pd.DataFrame(job_posts)
df.to_csv('job_posts.csv', mode='a', header=False)
