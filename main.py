import json
import tkinter as tk
from tkinter import simpledialog, messagebox
import requests
from bs4 import BeautifulSoup
from dicttoxml import dicttoxml
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import zipfile
import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the SQLAlchemy model
Base = declarative_base()

# Add a global variable to store the scraped results
scraped_results = []


class ScrapedData(Base):
    """
    A class to represent the scraped data model.
    """
    __tablename__ = 'scraped_data'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    category = Column(String)
    keyword = Column(String)


# Create a SQLAlchemy engine
engine = create_engine('postgresql://postgres:1379@localhost:5432/techcrunch_scraper')

# Create the table in the database
Base.metadata.create_all(engine)


def store_data_in_database(title, author, category, keyword):
    """
    Store the scraped data in a PostgreSQL database using SQLAlchemy.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    new_data = ScrapedData(title=title, author=author, category=category, keyword=keyword)
    session.add(new_data)
    session.commit()
    session.close()


def scrape_techcrunch(query, page_by_items):
    """
    Scrape the TechCrunch website and store the data in the database.
    """
    response = requests.get(f'https://search.techcrunch.com/search?p={query}&b={page_by_items}')
    soup = BeautifulSoup(response.text, 'html.parser')
    request_items = soup.find_all("a", attrs={'class': 'fz-20 lh-22 fw-b'})
    for request_item_detail in request_items:
        response_item_url = request_item_detail['href']
        response_item = requests.get(response_item_url)
        item_soup = BeautifulSoup(response_item.text, "html.parser")

        # Extracting author and category information
        author_tag = item_soup.find("div", class_="article__byline").find("a") if item_soup.find("div",
                                                                                                 class_="article__byline") else None
        author = author_tag.text.strip() if author_tag else 'Unknown Author'

        article_containers = item_soup.find_all(
            'div', class_=['article-container', 'article--post']
        )

        category = 'Unknown Category'  # Default

        # Search within each container
        for container in article_containers:
            category_tag = container.find(
                "a", class_="article__primary-category__link gradient-text gradient-text--green-gradient"
            )

            if category_tag:
                category = category_tag.text.strip()
                break  # Exit the loop once you've found the first occurrence

        # Store the data in the database
        store_data_in_database(item_soup.title.text, author, category,
                               query)
        scraped_results.append({
            'title': item_soup.title.text,
            'author': author,
            'category': category
        })


def generate_reports(output_folder, data, export_format):
    """
    Generate reports and export data in different formats based on the user's choice.
    """
    # Convert the data to the chosen export format
    if export_format == 'json':
        export_file_path = os.path.join(output_folder, 'report.json')
        with open(export_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    elif export_format == 'xml':
        export_file_path = os.path.join(output_folder, 'report.xml')
        xml_data = dicttoxml(data, custom_root='scraped_data', attr_type=False)
        with open(export_file_path, 'w') as xml_file:
            xml_file.write(xml_data.decode())
    else:  # Default to CSV if the format is not specified or invalid
        export_file_path = os.path.join(output_folder, 'report.csv')
        df = pd.DataFrame(data)
        df.to_csv(export_file_path, index=False)
    # Generate a bar chart showing the number of articles in each category
    df = pd.DataFrame(data)
    category_counts = df['category'].value_counts()
    category_counts.plot(kind='bar')
    plt.title('Number of Articles in Each Category')
    plt.xlabel('Category')
    plt.ylabel('Count')
    chart_path = os.path.join(output_folder, 'chart.png')
    plt.savefig(chart_path)

    # Generate a CSV report
    csv_file_path = os.path.join(output_folder, 'report.csv')
    df.to_csv(csv_file_path, index=False)

    # Generate an HTML report
    html_content = "<html><head><title>Scraped Data Report</title></head><body>"
    html_content += "<h1>Scraped Data Report</h1>"
    html_content += df.to_html()
    html_content += "</body></html>"
    html_file_path = os.path.join(output_folder, 'report.html')
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    # Create a folder for images
    media_folder = os.path.join(output_folder, 'media')
    os.makedirs(media_folder, exist_ok=True)
    os.replace(chart_path, os.path.join(media_folder, 'chart.png'))

    # Zip the output folder
    zip_file = output_folder + '.zip'
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        for root, dirs, files in os.walk(output_folder):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_folder))

    return export_file_path


def main():
    """
    Main function to prompt the user for input, perform web scraping, generate reports, and export data.
    """
    # Create a Tkinter GUI to prompt the user for the search query and page number
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    query = simpledialog.askstring("Input", "Enter the search query:")
    page = simpledialog.askinteger("Input", "Enter the page number:")

    # Prompt the user to choose the export format
    export_format = simpledialog.askstring("Export Format", "Choose the export format (json, xml, or csv):").lower()

    if export_format in ['json', 'xml', 'csv']:
        # Perform web scraping
        scrape_techcrunch(query, ((page - 1) * 10) + 1)

        # Generate reports and export data
        output_folder = f"{query}_{datetime.date.today()}"
        os.makedirs(output_folder, exist_ok=True)

        # Use the scraped results to generate reports and export data
        zip_file = generate_reports(output_folder, scraped_results, export_format)

        print(f"Reports generated and data exported in {export_format} format.")
        print(f"Export file created: {zip_file}")
    else:
        messagebox.showerror("Error", "Invalid export format. Please choose 'json', 'xml', or 'csv'.")


if __name__ == "__main__":
    main()
