import requests
from bs4 import BeautifulSoup
import csv

# Function to get data from Amazon based on a search term
def scrape_amazon(keyword):
    url = f"https://www.amazon.in/s?k={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    # Create a list of products (name, price, and rating)
    product_data = []
    for product in products:
        name = product.find('span', class_='a-text-normal')
        price = product.find('span', class_='a-price-whole')
        rating = product.find('span', class_='a-icon-alt')
        
        if name and price and rating:
            product_data.append([name.text.strip(), price.text.strip(), rating.text.strip()])
    
    return product_data

# Function to save the data into a CSV file
def save_to_csv(data, filename="amazon_products.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Name', 'Price', 'Rating'])
        writer.writerows(data)

if __name__ == "__main__":
    search_term = input("Enter search keyword: ")
    product_data = scrape_amazon(search_term)
    save_to_csv(product_data)
    print(f"Data saved to amazon_products.csv")
