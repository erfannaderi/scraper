# TechCrunch Scraper

This Python scraper uses the `requests` library and `BeautifulSoup` (bs4) to extract articles from TechCrunch based on keywords and categories. It provides three different ways to access the scraped data.

## Features
- **CLI**: Obtain results by keyword or based on a preselected category.
- **Simple GUI**: Search by keyword.
- **Advanced GUI**: Generate a graph and export data in CSV or JSON format from a keyword search and authors' names.

## Installation
1. Clone the repository using the following Git address: [https://github.com/erfannaderi/scraper](https://github.com/erfannaderi/scraper)
2. Install the required dependencies by running the following command:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To use the scraper, run the `scraper.py` script from the command line. This will prompt the user for the search query, page number, and export format. The scraper will then perform web scraping, generate reports, and export data based on the user's input.

## Requirements
- Python 3.x
- `requests`
- `beautifulsoup4`
- `dicttoxml`
- `sqlalchemy`
- `pandas`
- `matplotlib`

## Database
The scraped data is stored in a PostgreSQL database using SQLAlchemy. The database table `scraped_data` contains the following columns:
- `id` (Primary Key)
- `title`
- `author`
- `category`
- `keyword`

## Contributing
Contributions to the project are welcome! If you'd like to contribute, please submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
