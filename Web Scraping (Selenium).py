print("⏳\n importing libraries⏳\n")
from selenium import webdriver #used to access sites like a pro
from selenium.webdriver.firefox.options import Options #used to tweak site accessing behaviour
from bs4 import BeautifulSoup #used to extract data

URL = "https://finance.yahoo.com/quote/BTC-USD/history/"

def get_html_content():
    options = Options()
    options.add_argument("--headless") 

    driver = webdriver.Firefox(options=options)
    try:
        driver.get(URL)
        print("\n⏳ Loading Page...⏳\n")
        html = driver.page_source
    finally:
        driver.quit()

    return html

def get_prices():
    html = get_html_content()
    dates, prices = [], []

    table = BeautifulSoup(html, "html.parser")
    table = table.find("table").find("tbody")

    for tr in table.findChildren("tr"):
        trs = tr.findChildren("td")
        date = "".join(trs[0].text.split(","))
        close_price = trs[-2].text
        close_price = "".join(close_price.split(","))

        prices.append(close_price)
        dates.append(date)
    return list(zip(dates, prices))

def save_data():
    with open("btc_prices.csv", "w") as pr:
        print("CSV file created ✅")
        data = get_prices()
        if not data:
            print("Problem finding prices table❌")
        else:
            pr.write("Dates,Prices\n")
            for data in data:
                content = data[0] + "," + data[1] + "\n"
                pr.write(content)
            print("Data saved successfully ✅")

save_data()