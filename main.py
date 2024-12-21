import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import json

# InfinityFree मा डाटा पठाउने function
def upload_to_website(data):
    url = "https://raaju.infy.uk/upload.php"  # तपाईंको upload.php endpoint
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Data uploaded successfully!")
        else:
            print(f"Failed to upload data: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error uploading data: {e}")

# नेप्से अल्फा वेबसाइटबाट डाटा स्क्रैप गर्ने function
def scrape_nepse_data():
    try:
        url = "https://nepsealpha.com/live-market"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        stock_data = []
        table = soup.find("table", {"class": "table"})  # सही class राख्नुहोस्
        rows = table.find_all("tr")[1:]  # Header line हटाउने

        for row in rows:
            cols = row.find_all("td")
            stock_data.append({
                "Stock": cols[0].text.strip(),
                "Close": float(cols[1].text.strip()),
                "%Change": float(cols[2].text.strip()),
                "High": float(cols[3].text.strip()),
                "Low": float(cols[4].text.strip()),
                "Volume": int(cols[5].text.strip().replace(',', '')),
                "Turnover": float(cols[6].text.strip().replace(',', ''))
            })

        return stock_data
    except Exception as e:
        print(f"Error scraping data: {e}")
        return None

# नेपाली समय निकाल्ने function
def get_nepali_time():
    utc_time = datetime.utcnow()
    nepali_time = utc_time + timedelta(hours=5, minutes=45)
    return nepali_time

# मुख्य flow
def update_data():
    last_data = None  # 15:05 को डाटा स्टोर गर्न
    thursday_data = None  # बिहीबारको 15:05 को डाटा स्टोर गर्न

    while True:
        now = get_nepali_time()
        day = now.strftime("%A")
        current_time = now.strftime("%H:%M")

        # शुक्रवार र शनिवारमा बिहीबारको डाटा प्रयोग
        if day in ["Friday", "Saturday"]:
            if thursday_data:
                print(f"Using Thursday's data for {day}.")
                upload_to_website(thursday_data)
            else:
                print("No Thursday data available yet.")
        else:
            # 10:30 देखि 15:05 को बीचमा डाटा स्क्रैप गर्ने
            if "10:30" <= current_time <= "15:05":
                print(f"Scraping data at {current_time}...")
                scraped_data = scrape_nepse_data()
                if scraped_data:
                    last_data = scraped_data  # 15:05 को डाटा अपडेट गर्न
                    if day == "Thursday":
                        thursday_data = scraped_data  # बिहीबारको डाटा सेभ गर्ने
                    upload_to_website(scraped_data)
                else:
                    print("Failed to scrape data.")
            else:
                # बाँकी समयमा 15:05 को डाटा प्रयोग गर्ने
                if last_data:
                    print(f"Using last data (15:05) for {current_time}.")
                    upload_to_website(last_data)
                else:
                    print("No last data available.")

        # 10 minutes कुर्नुहोस्
        time.sleep(600)  # 600 seconds = 10 minutes

if __name__ == "__main__":
    update_data()