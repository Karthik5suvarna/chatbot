# import requests
# from bs4 import BeautifulSoup
# import json

# def scrape_aiotrix():
#     base_url = "https://www.aiotrix.com"
#     pages = [
#         "", 
#         "/about-us", 
#         "/services", 
#         "/careers", 
#         "/contact-us",
#         "/services/artificial-intelligence",
#         "/services/iot-solutions",
#         "/services/data-analysis-and-visualization",
#         "/services/product-development-and-mvp-development",
#         "/services/mobile-application-development",
#         "/services/industry-4-automation",
#         "/blogs/project-ekalavya",
#         "/blogs/flutter-optimization",
#         "/careers/ekalavya/apprenticeship",
#         "/careers/ekalavya/internship",
#         "/careers/ekalavya/seminars",
#         "/terms-and-conditions",
#         "/privacy-policy"
#     ]
#     data = {}

#     for page in pages:
#         url = base_url + page
#         response = requests.get(url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.content, "html.parser")
#             texts = soup.get_text(separator=" ").strip()
#             data[page] = texts
#         else:
#             print(f"Failed to retrieve {url}")

#     # Save to JSON file
#     with open("aiotrix_data.json", "w") as f:
#         json.dump(data, f, indent=4)

# if __name__ == "__main__":
#     scrape_aiotrix()



import requests
from bs4 import BeautifulSoup
import json
import re

# List of URLs to scrape
urls = [
    'https://www.aiotrix.com',
    'https://www.aiotrix.com/services/artificial-intelligence',
    'https://www.aiotrix.com/services/iot-solutions',
    'https://www.aiotrix.com/services/data-analysis-and-visualization',
    'https://www.aiotrix.com/services/product-development-and-mvp-development',
    'https://www.aiotrix.com/services/mobile-application-development',
    'https://www.aiotrix.com/services/industry-4-automation',
    'https://www.aiotrix.com/blogs/project-ekalavya',
    'https://www.aiotrix.com/blogs/flutter-optimization',
    'https://www.aiotrix.com/careers/ekalavya/apprenticeship',
    'https://www.aiotrix.com/careers/ekalavya/internship',
    'https://www.aiotrix.com/careers/ekalavya/seminars',
    'https://www.aiotrix.com/terms-and-conditions',
    'https://www.aiotrix.com/privacy-policy'
]

# Function to scrape content from a URL
def scrape_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Scrape content from each URL and store in a dictionary
data = {}
for url in urls:
    content = scrape_content(url)
    data[url] = content

# Save the data to a JSON file
with open('aiotrix_data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Data scraping completed and saved to aiotrix_data.json")
