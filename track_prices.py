import requests
from bs4 import BeautifulSoup
import smtplib

URL = input("Link the page here: ").strip()
pages = int(input("How many pages? "))
maximum_price = float(input("What is the maximux price? [ex: 2.999] "))

headers = {
    "User-Agent": 'your user agent'}

mail_product_list = []


def check_price():
    for i in range(0, pages):
        if i == 1:
            count = 49
            NEW_URL = URL + f"_Desde_{count}"
        if i > 1:
            count += 48
            NEW_URL = URL + f"_Desde_{count}"
        if i == 0:
            page = requests.get(URL, headers=headers)
        else:
            page = requests.get(NEW_URL, headers=headers)

        soup = BeautifulSoup(page.content, "html.parser")

        links = soup.find_all(attrs={"class": "item__info-link item__js-link"})

        for link in links:
            prices = link.find_all(attrs={"class": "price__fraction"})
            for price in prices:
                converted_price = float(price.get_text())

                if converted_price <= maximum_price:
                    mail_product_list.append(
                        f"This is a small price of: {converted_price:4.3f}")
                    mail_product_list.append(
                        f"This is the link: \n{link['href']}")
    send_email()


def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('your_email', 'password')

    subject = "This prices are for you!"
    body = ""
    for mail in mail_product_list:
        body += f"{mail}\n"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'from',
        'to',
        msg
    )
    server.quit()


check_price()
