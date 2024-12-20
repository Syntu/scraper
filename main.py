import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime, timedelta

# InfinityFree मा डाटा पठाउने function
def upload_to_website(data):
    url = "https://your-infinityfree-website.com/api_endpoint"  # तपाईंको endpoint
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Data uploaded successfully!")
    else:
        print("Failed to upload data:", response.status_code)

# नेप्सेबाट डाटा स्क्रैप गर्ने function
def scrape_nepse_data():
    try:
        response = requests.get("https://nepsealpha.com/live-market")
        soup = BeautifulSoup(response.content, "html.parser")

        # तपाईंले आवश्यक डाटा स्क्रैप गर्ने logic
        stock_data = []
        table = soup.find("table", {"class": "table"})  # Replace with the correct table class
        rows = table.find_all("tr")[1:]  # Skip header row

        for row in rows:
            cols = row.find_all("td")
            stock_data.append({
                "Stock": cols[0].text.strip(),
                "Close": cols[1].text.strip(),
                "%Change": cols[2].text.strip(),
                "High": cols[3].text.strip(),
                "Low": cols[4].text.strip(),
                "Volume": cols[5].text.strip(),
                "Turnover": cols[6].text.strip(),
            })
        
        return stock_data
    except Exception as e:
        print("Error scraping data:", e)
        return None

# नेपाली समयका लागि function
def get_nepali_time():
    utc_time = datetime.utcnow()
    nepali_time = utc_time + timedelta(hours=5, minutes=45)
    return nepali_time

# टाइम अनुसार schedule गर्ने function
def update_data():
    now = get_nepali_time()
    day = now.strftime("%A")
    if day in ["Friday", "Saturday"]:
        print("Today is", day, "- Using Thursday's data.")
    else:
        data = scrape_nepse_data()
        if data:
            upload_to_website(data)

# Schedule settings (नेपाली समय अनुसार)
def start_scheduling():
    schedule.every().day.at("10:30").do(update_data)
    schedule.every(1).minutes.do(update_data).tag('market_hours')

    while True:
        current_time = get_nepali_time().strftime("%H:%M")
        if current_time == "15:05":
            schedule.clear('market_hours')  # बजार समयपछि scheduler हटाउने
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduling()