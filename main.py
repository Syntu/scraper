import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import schedule
import time

# InfinityFree मा डाटा पठाउने function
def upload_to_website(data):
    url = "https://raaju.infy.uk/upload.php"  # तपाईंको upload.php endpoint
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Data uploaded successfully!")
        else:
            print("Failed to upload data:", response.status_code, response.text)
    except Exception as e:
        print("Error uploading data:", e)

# नेप्सेबाट डाटा स्क्रैप गर्ने function
def scrape_nepse_data():
    try:
        response = requests.get("https://nepsealpha.com/live-market")
        soup = BeautifulSoup(response.content, "html.parser")

        stock_data = []
        # यहाँ तपाईंको तालिका पहिचान गर्ने कोड सही गर्नुपर्नेछ
        table = soup.find("table", {"class": "table"})  # Table class replace गर्नुहोस्
        rows = table.find_all("tr")[1:]  # Header line skip गर्ने

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
        print("Error scraping data:", e)
        return None

# नेपाली समय निकाल्ने function
def get_nepali_time():
    utc_time = datetime.utcnow()
    nepali_time = utc_time + timedelta(hours=5, minutes=45)
    return nepali_time

# मुख्य कार्य flow
def update_data():
    now = get_nepali_time()
    day = now.strftime("%A")
    if day in ["Friday", "Saturday"]:
        print(f"Today is {day}. Using Thursday's data.")
        # बिहीबारको डाटा प्रयोग गर्ने अन्य function राख्न सक्नुहुन्छ
    else:
        data = scrape_nepse_data()
        if data:
            upload_to_website(data)

# Schedule settings
def start_scheduling():
    schedule.every().day.at("10:30").do(update_data)
    schedule.every(1).minutes.do(update_data).tag("market_hours")

    while True:
        current_time = get_nepali_time().strftime("%H:%M")
        if current_time == "15:05":
            schedule.clear("market_hours")  # बजार समयपछि scheduler हटाउने
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduling()
