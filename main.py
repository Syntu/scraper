import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

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

# मुख्य कार्य flow
def update_data():
    now = get_nepali_time()
    day = now.strftime("%A")
    if day in ["Friday", "Saturday"]:
        print(f"Today is {day}. Using Thursday's data.")  # बिहीबारको डाटा प्रयोग गर्न सेटअप गर्नुहोस्।
    else:
        data = scrape_nepse_data()
        if data:
            upload_to_website(data)

if __name__ == "__main__":
    update_data()
