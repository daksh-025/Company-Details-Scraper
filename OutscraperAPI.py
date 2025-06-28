import json
import requests
import pandas as pd
import time

# API Credentials
HOST = "api.scrapeless.com"
URL = f"https://{HOST}/api/v1/scraper/request"
TOKEN = "sk_0zCbnwy9afWVL4ci8Snj6uA71dlvvOe1JTRzC6UipE0Ta66nthgGipe0y0sLLYIz"

def fetch_company_info(company_name, search_type="website"):
    headers = {"x-api-token": TOKEN}
    
    search_queries = {
        "website": f"{company_name} UK company official site",
        "linkedin": f"{company_name} company LinkedIn"
    }

    json_payload = json.dumps({
        "actor": "scraper.google.search",
        "input": {
            "q": search_queries[search_type],
            "gl": "us",
            "hl": "en",
            "google_domain": "google.com"
        }
    })
    
    response = requests.post(URL, headers=headers, data=json_payload)
    if response.status_code != 200:
        print(f"Error {search_type} for {company_name}: {response.status_code}, {response.text}")
        return "Not Found"

    response_data = response.json()
    if "organic_results" in response_data and len(response_data["organic_results"]) > 0:
        return response_data["organic_results"][0]["link"]
    
    return "Not Found"

# Load Excel file
df = pd.read_excel("newforhenry.xlsx")  # Change filename if needed

# Process first 10 rows
df = df.head(100)
df["Company Website"] = ""
df["Company LinkedIn"] = ""

for index, row in df.iterrows():
    company_name = row["CompanyName"]  # Adjust column name if needed
    print(f"Processing: {company_name}")
    
    website = fetch_company_info(company_name, "website")
    linkedin = fetch_company_info(company_name, "linkedin")
    
    df.at[index, "Company Website"] = website
    df.at[index, "Company LinkedIn"] = linkedin
    
    time.sleep(2)  # Prevent hitting API rate limits

# Save updated Excel
df.to_excel("updated_companies.xlsx", index=False)
print("Process completed. Data saved to updated_companies.xlsx")
