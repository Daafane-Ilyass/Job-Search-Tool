from bs4 import BeautifulSoup
import requests
import re

def extract_days_ago(date_string):
    if 'few' in date_string:
        return 0
    else:
        match = re.search(r'(\d+)', date_string)
        if match:
            return int(match.group())
        else:
            return -1

if __name__ == '__main__':
    skill = input("Enter your skills: ").replace(' ', '+')
    location = input("Enter the desired job location(s): ").replace(' ', '+')
    max_days_ago = int(input("Enter the maximum number of days since the job offer was posted: "))

    url = f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={skill}&txtLocation={location}'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    posting_dates = soup.find_all('span', class_='sim-posted')
    job_titles = soup.select('h2 > a')

    counter = 0

    for idx in range(len(job_titles)):
        days_ago = extract_days_ago(str(posting_dates[idx]))
        if days_ago >= 0 and days_ago <= max_days_ago:
            job_title = job_titles[idx].text.strip()
            posting_date = posting_dates[idx].text.strip()
            job_link = job_titles[idx]['href']

            print(f"Job Title: {job_title}")
            print(f"Posting Date: {posting_date}")
            print(f"Job Link: {job_link}")
            print()
            counter += 1

    if counter == 0:
        print("We couldn't find a job that matches your criteria!")
    else:
        print(f"We found {counter} jobs that match your criteria!")
