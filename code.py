# Import necessary libraries for web scraping, data handling, and automation
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import numpy as np
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import csv

# Read CSV file containing review links and load into a DataFrame
df = pd.read_csv('Final_review_links_s.csv')

# Open CSV file for reading review links data
file = open('Final_review_links_s.csv', "r")
csv_reader = csv.reader(file)

# Initialize lists to store extracted data
lists = []
for row in csv_reader:
    lists.append(row)

# The lists structure
# lists[i][1] represents product category
# lists[i][2] represents software name
# lists[i][3] represents URL

copy_list = lists

# Initialize empty lists to store final data for various fields
overall = []
alter_res = []
reason_choose_res = []
recomm_res = []
reason_switch_res = []
rev_date = []
rev_source = []
cons_res = []
pros_res = []
overall_res = []
switch_from_res = []
name_list = []
designation = []
industry = []
size = []
usage_duration = []
heading = []
industry_and_size = []
software_name = []
product_category = []
list2 = []
industry = []
size = []
list3 = []

# Dictionaries to store data categories for each review field
data1 = {
    'Alternatives Considered:': [],
    'Pros:': [],
    'Cons:': [],
    'Overall:': [],
    'Reasons for Choosing': [],
    "Recommendations to other buyers:": [],
    'Reasons for Switching to': [],
    "Switched From:": []
}

# Dictionary for detailed reviewer information
datad = {
    'Designation': [],
    'Usage': [],
    'Industry&size': [],
    'heading': [],
    'overall': [],
    'Name': [],
    'Overall Rating': [],
    'Ease of Use': [],
    'Customer Service': [],
    'Features': [],
    'Value for Money': [],
    'Likelihood to Recommend': []
}

# Define the scraping function to extract data from each review page
def scrapper():
    global copy_list
    for i, n in enumerate(copy_list):
        print(i)
        # Continue from the 2nd item to allow for previous iteration stops
        if i == 1:
            copy_list = lists[i:]
            break

        # Pause between each request to prevent server overload
        time.sleep(1)
        
        # Extract category, software name, and URL for each review
        category = n[1]
        name = n[2]
        url = n[3]
        
        # Setup Chrome WebDriver service for web scraping
        s = Service('/Users/seharaejaz/Downloads/chromedriver 2')
        driver = webdriver.Chrome(service=s)
        
        # Open review URL in Chrome browser
        driver.get(url)
        time.sleep(2)

        # Create an ActionChains object for automated scrolling
        action = ActionChains(driver)
        
        # Scroll down the page to load content dynamically
        for i in range(95):
            action.send_keys(Keys.SPACE).perform()
            time.sleep(1)

        # Find main review section on the page
        x = driver.find_element_by_class_name('gtm-review-section')
        
        # Locate all review elements with class "nb-flex-grow"
        w = driver.find_elements_by_class_name("nb-flex-grow")
        ov = []

        # Extract text content of each review element
        for i in w:
            ov.append(i.get_attribute('textContent'))

        # Process and split the review content into fields
        for i in range(0, len(w), 2):
            l = w[i].text.split('\n')
            
            # Append the reviewer's name and rating information
            datad['Name'].append(l[0])
            feat = ['Overall Rating', 'Ease of Use', 'Customer Service', 'Features', 'Value for Money', 'Likelihood to Recommend']
            
            # Extract each feature rating for the reviewer
            for i in feat:
                if i in l:
                    datad[i].append(l[l.index(i) + 1])
                else:
                    datad[i].append(-1)

        # Process right-side data of each review
        for i in range(1, len(w), 2):
            l = w[i].text.split('\n')
            print(l)
            heading.append(l[0])
            feat2 = ['Alternatives Considered:', 'Overall:', 'Pros:', 'Cons:', 'Reasons for Choosing', "Recommendations to other buyers:", 'Reasons for Switching to', "Switched From:"]

            # Extract each relevant field for the review's right side
            for i in feat2:
                t = 0
                for j in l:
                    if i in j:
                        t = 1
                        data1[i].append(j[j.index(':') + 1:])
                if t == 0:
                    data1[i].append(-1)

        # Track the names for counting total reviews
        names = datad['Name']
        num = len(names)

        # Append specific data for each review entry
        for i in w:
            i = i.find_elements_by_class_name("nb-text-gray-300")
            list1 = []
            for j in i:
                list1.append(j.text)
            list2.append(list1)
        
        # Append category and software name data
        for i in range(int(len(driver.find_elements_by_class_name("nb-flex-grow")) / 2)):
            software_name.append(name)
            product_category.append(category)

        # Close the browser window
        driver.quit()

# Execute the scraper function
scrapper()

# Process list2 data to create list3 with industry and size data
for i in range(0, len(list2), 2):
    list3.append(list2[i])

# Append extracted information to designated lists
for i in list3:
    if i != []:
        designation.append(i[0])
        industry_and_size.append(i[1])
        usage_duration.append(i[2])
        rev_date.append(i[-1].split('\n')[-1])
        rev_source.append(i[-1].split('\n')[-2])
    else:
        designation.append(' ')
        industry_and_size.append(' ')
        usage_duration.append(' ')
        rev_date.append('')
        rev_source.append('')

# Use regex to extract industry and company size information
import re
for i in industry_and_size:
    if i == 'Unspecified':
        industry.append('Unspecified')
        size.append('Unspecified')
    elif i == 'Self-employed':
        industry.append('Self-employed')
        size.append('Self-employed')
    else:
        n = re.search(r'\d', i)
        if n is not None and n.start() != 0:
            industry.append(i[0:n.start() - 2])
            size.append(i[n.start():])
        elif n is not None and n.start() == 0:
            industry.append('Unspecified')
            size.append(i)
        else:
            industry.append(i)
            size.append('Self-Employed')

# Prepare the final data for DataFrame creation
data_final = {
    'Software name': software_name,
    'Product category': product_category,
    'Name': datad['Name'],
    'Designation': designation,
    'Industry & Size': industry_and_size,
    'Industry': industry,
    'Company Size': size,
    'Usage Duration': usage_duration,
    'Heading': heading,
    'Overall': data1['Overall:'],
    'Pros': data1['Pros:'],
    'Cons': data1['Cons:'],
    'Reviewer Source ': rev_source,
    'Review Date': rev_date,
    'Alternatives': data1['Alternatives Considered:'],
    'Reason for choosing the software': data1['Reasons for Choosing'],
    'Reason for switching to the software': data1['Reasons for Switching to'],
    'Switched from': data1["Switched From:"],
    'Overall Rating': datad['Overall Rating'],
    'Ease of Use': datad['Ease of Use'],
    'Customer Service': datad['Customer Service'],
    'Features': datad['Features'],
    'Value for Money': datad['Value for Money'],
    'Likelihood to Recommend': datad['Likelihood to Recommend']
}

# Create DataFrame from the collected data and save to CSV
dff = pd.DataFrame(data_final)
dff.head(250)  # Display the first 250 rows
dff.to_csv('practicefus.csv')  # Save DataFrame to CSV
