# import requests
# from bs4 import BeautifulSoup
#
# from constatns import SEARCH_BASE_URL, ITEM_CLASS
#
# # pagination search input
# page_input = int(input("enter the page number: "))
# if page_input >= 1:
#     page_by_items = ((page_input - 1) * 10) + 1
# else:
#     page_by_items = 10
# # query search input
# query = input('enter search: ')
# response = requests.get(SEARCH_BASE_URL.format(query=query, page_by_items=page_by_items))
# # print(response.status_code)
# # print(response.url)
# # print(dir(response))
# # print(response.text)
# soup = BeautifulSoup(response.text, 'html.parser')
# # print(soup.prettify())
# # print(soup.title)
# # print(soup.title.string)
# # print(soup.title.text)
# # single / detail page finds
# request_item = soup.find_all("a", attrs={'class': ITEM_CLASS})
# for request_item_detail in request_item:
#     # print(request_item_detail)
#     # print(request_item_detail['href'])
#     response_item_url=request_item_detail['href']
#     # print("text: ", request_item_detail.text)
#     response_item = requests.get(response_item_url)
#     item_soup = BeautifulSoup(response_item.text, "html.parser")
#     print(response_item.status_code)
#     print(response_item.url)
#     print("item_soap: ", item_soup.title.text)
import requests
from bs4 import BeautifulSoup

from constatns import SEARCH_BASE_URL, ITEM_CLASS


def main():
    """
    Main function to perform the web scraping and item retrieval.
    """
    # Pagination search input
    page_input = int(input("Enter the page number: "))
    if page_input >= 1:
        page_by_items = ((page_input - 1) * 10) + 1
    else:
        page_by_items = 10  # Default to 10 if the input is invalid

    # Query search input
    query = input('Enter the search query: ')

    # Send a GET request to the search URL
    response = requests.get(SEARCH_BASE_URL.format(query=query, page_by_items=page_by_items))

    # Parse the response content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all items with the specified class
    request_items = soup.find_all("a", attrs={'class': ITEM_CLASS})

    # Process each item
    for request_item_detail in request_items:
        response_item_url = request_item_detail['href']
        # Send a GET request to the item URL
        response_item = requests.get(response_item_url)
        item_soup = BeautifulSoup(response_item.text, "html.parser")
        print(response_item.status_code)
        print(response_item.url)
        print("Item title: ", item_soup.title.text)


if __name__ == "__main__":
    main()

# def main():
#     # Parse command-line arguments
#     parser = argparse.ArgumentParser(description='TechCrunch Web Scraper')
#     parser.add_argument('query', type=str, help='Search query')
#     parser.add_argument('page', type=int, help='Page number')
#     args = parser.parse_args()
#
#     # Perform web scraping
#     scrape_techcrunch(args.query, ((args.page - 1) * 10) + 1)
#
#     # Generate reports and export data
#     output_folder = f"{args.query}_{datetime.date.today()}"
#     os.makedirs(output_folder, exist_ok=True)
#     zip_file = generate_reports(output_folder)
#
#     print(f"Reports generated and data exported.")
#     print(f"Zip file created: {zip_file}")
#
#
# if __name__ == "__main__":
#     main()
