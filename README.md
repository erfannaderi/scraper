TechCrunch Scraper with Report Generation
This Python script scrapes articles from TechCrunch based on a user-provided search query and page number. It then stores the scraped data in a PostgreSQL database and generates reports with various export formats and visualizations.

Features:

Scrapes TechCrunch articles based on searcgit inith query and page number.
Stores scraped data (title, author, category, keyword) in a PostgreSQL database.
Generates reports with the following options:
JSON
XML
CSV
Bar chart showing article count by category
Zips the report folder for easy distribution.
User-friendly Tkinter GUI for input (search query, page number, export format)
Requirements:

This script requires the following Python libraries:

requests: Makes HTTP requests to TechCrunch.
beautifulsoup4: Parses HTML content.
dicttoxml: Converts dictionaries to XML format (optional for XML reports).
sqlalchemy: Connects to and interacts with the PostgreSQL database.
pandas: Used for data manipulation and creating CSV reports.
matplotlib.pyplot: Creates bar charts.
tkinter: Provides a GUI for user input.
zipfile: Zips the reports folder.
Installation:

Create a virtual environment: It's recommended to use a virtual environment to isolate project dependencies. You can use tools like venv or virtualenv for this purpose.

Activate the virtual environment: Refer to your chosen tool's documentation for activation instructions.

Install dependencies: Open a terminal or command prompt and navigate to your project directory. Run the following command to install all required libraries from the requirements.txt file:

Bash
pip install -r requirements.txt
Use code with caution.
Usage:

Run the script: Execute the script using python main.py in your terminal.
User Input: The script will prompt you for the following information:
Search query: Enter the keyword or topic you want to scrape articles about.
Page number: Enter the specific page number of TechCrunch search results you want to scrape (starts from 1).
Export format: Choose the format for your reports (JSON, XML, or CSV).
Report Location:

The script will generate a folder named query_date (where query is your search term and date is the current date) containing the following report files:

report.EXTENSION (where EXTENSION is the chosen export format)
chart.png (Bar chart showing article count by category)
report.html (HTML report summarizing the scraped data)
report.csv (CSV report, always generated regardless of chosen format)
report.zip (Zipped archive of the entire report folder)
Database Setup (Optional):

This script assumes a PostgreSQL database named techcrunch_scraper is available. You'll need to create this database and configure the connection details in the script (engine variable) if you want to store scraped data.

Disclaimer:

This script is for educational purposes only. Please respect TechCrunch's robots.txt and terms of use while using this scraper.

Author: Erfan Naderi