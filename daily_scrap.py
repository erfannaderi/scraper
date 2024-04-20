import requests
from bs4 import BeautifulSoup
from dateutil.utils import today


# Function to scrape TechCrunch articles from a specific day
def scrape_techcrunch_articles(date_str):
    url = f"https://techcrunch.com/{date_str}/"  # Format the URL with the desired date

    session = requests.Session()
    session.max_redirects = 1000 # Allow unlimited redirects

    response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = soup.find_all("div", class_="post-block-content")

    for article in articles:
        article_title = article.find("h2", class_="post-block__title").find("a").get_text()
        article_url = article.find("h2", class_="post-block__title").find("a")["href"]
        article_author = article.find("span", class_="river-byline__authors").find("a").get_text()

        # Extract the article details by visiting the article URL
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.content, "html.parser")

        article_text = article_soup.find("div", class_="article-content").get_text(strip=True)
        article_category = article_soup.find("a", class_="article__category").get_text()

        print("Article Title:", article_title)
        print("Article URL:", article_url)
        print("Author:", article_author)
        print("Text:", article_text)
        print("Category:", article_category)
        print("-----")
        # You can store the data in a database, file, or perform any other desired actions


# Specify the desired date as "YYYY/MM/DD"
date_str = today

# Call the scraper function for the specified date
scrape_techcrunch_articles(date_str)
