import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

data = []

# Scrape first 5 pages
for page in range(1, 6):

    url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    response = requests.get(url)

    print("Scraping page:", page)

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books:

        title = book.h3.a["title"]

        price = book.find(
            "p", class_="price_color"
        ).text

        availability = book.find(
            "p", class_="instock availability"
        ).text.strip()

        rating = book.find(
            "p", class_="star-rating"
        )["class"][1]

        data.append({
            "Title": title,
            "Price": price,
            "Availability": availability,
            "Rating": rating
        })


# Create DataFrame
df = pd.DataFrame(data)


# Clean Price column
df["Price"] = (
    df["Price"]
    .str.extract(r"(\d+\.\d+)")[0]
    .astype(float)
)


# Create custom Price Category
def price_category(price):

    if price < 20:
        return "Low"

    elif price < 40:
        return "Medium"

    else:
        return "High"


df["Price Category"] = df["Price"].apply(price_category)


# Save dataset
df.to_csv("books_dataset_5_pages.csv", index=False)


# Display basic analysis
print("\nScraping completed!")
print("Total records:", len(df))

print("\nFirst 5 records:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nAverage Price:")
print(df["Price"].mean())

print("\nMaximum Price:")
print(df["Price"].max())

print("\nMinimum Price:")
print(df["Price"].min())

print("\nRating Count:")
print(df["Rating"].value_counts())

print("\nPrice Category Count:")
print(df["Price Category"].value_counts())


# Create visualization
category_counts = df["Price Category"].value_counts()

category_counts.plot(kind="bar")

plt.title("Books by Price Category")
plt.xlabel("Price Category")
plt.ylabel("Number of Books")

plt.tight_layout()

plt.savefig("price_category_chart.png")

plt.show()