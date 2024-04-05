from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import datetime
import smtplib
import csv
from dotenv import load_dotenv, dotenv_values

config = dotenv_values(".env")

# with open('csv/AmazonWebScrappingDataset.csv','w',newline='',encoding='UTF8') as f:
#     writer=csv.writer(f)
#     writer.writerow(header)
#     writer.writerow(data)

# df=pd.read_csv("csv/AmazonWebScrappingDataset.csv")
# print(df)



def send_mail():
    email = config['MAIL']
    passo = config['PASS']
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    # server.starttls()
    server.ehlo()
    server.login(email, passo)

    subject = "The Shoe you want is below 10000! Now is your chance to buy!"
    body = "Ketan, This is the moment we have been waiting for. Now is your chance to pick up the shirt of your " \
           "dreams. Don't mess it up! Link here: " \
           "https://www.amazon.in/Puma-Unisex-Adult-RS-Trck-Silver-White-Sneaker/dp/B0CT89DYJ4/ref=sr_1_30?sr=8-30"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        email,
        msg

    )


def check_price():
    ua = config['USER_AGENT']
    url = 'https://www.amazon.in/Puma-Unisex-Adult-RS-Trck-Silver-White-Sneaker/dp/B0CT89DYJ4/ref=sr_1_30?sr=8-30'
    headers = {"User-Agent": ua}
    page = requests.get(url, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    title = soup2.find(id="productTitle").get_text()
    price = soup2.find('span', {'class': 'a-price-whole'}).get_text()
    price = price.strip()
    title = title.strip()
    today = datetime.date.today()
    header = ['Title', 'Price', 'Date']
    data = [title, price, today]
    str_price = ""
    for i in range(0, len(price)):
        if (price[i] != ","):
            str_price += price[i]
    str_price = int(str_price)

    with open('csv/AmazonWebScrappingDataset.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    if (str_price < 10000):
        send_mail()


check_price()
