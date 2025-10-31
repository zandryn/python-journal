import requests
from bs4 import BeautifulSoup
import csv

# sample site
url = "https://www.reikowakai.com/"

response = requests.get(url)

print(response.text)
soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())

quotes = []
quote_boxes = soup.find_all('div', class_='col-6 col-lg-3 text-center margin-30px-bottom sm-margin-30px-top')
for box in quote_boxes:
    quote_text = box.img['alt'].split(" #")
    quote = {
        'theme': box.h5.text.strip(),
        'image_url': box.img['src'],
        'lines': quote_text[0],
        'author': quote_text[1] if len(quote_text) > 1 else 'Unknown'
    }
    quotes.append(quote)

# Display extracted quotes
for q in quotes[:5]:  # print only first 5 for brevity
    print(q)

filename = "quotes.csv"
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['theme', 'image_url', 'lines', 'author'])
    writer.writeheader()
    for quote in quotes:
        writer.writerow(quote)