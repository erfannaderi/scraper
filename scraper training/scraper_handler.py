import requests
from bs4 import BeautifulSoup
from constatns import ITEM_CLASS
from models import ArticleSearchByKeywordItem, Article, Author, Category, ArticleCategory, SearchByKeyword, Keyword


class ScraperHandler:
    def __init__(self, base_url, search_url):
        self.base_url = base_url
        self.search_url = search_url

    def request_to_target_url(self, url):
        print('URL:', url)
        return requests.get(url)

    def search_by_keyword(self, search_by_keyword_instance):
        search_items = list()

        for i in range(1, search_by_keyword_instance.page_count+1):
            response = self.request_to_target_url(
                self.search_url.format(
                    query=search_by_keyword_instance.keyword,
                    page=i,
                    search_type=search_by_keyword_instance,
                )
            )

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                search_items += self.extract_search_items(
                    search_by_keyword=search_by_keyword_instance,
                    soup=soup
                )

        if search_by_keyword_instance:
            for search_item in search_items:
                article, category = self.parse_book_detail(url=search_item.url)
                data = {
                    'title': article.title,
                    'author': article.author.fullname,
                    'description': article.description,
                    'category': category,
                }
                print(data)
        return search_items

    def extract_search_items(self, search_by_keyword, soup):
        search_items = list()

        search_result_item = soup.findAll(
            'a',
            attrs={'class': ITEM_CLASS[search_by_keyword.search_type]}
        )

        for a in search_result_item:
            search_items.append(self.parse_search_item(search_by_keyword=search_by_keyword, a_tag=a))

        return search_items

    def parse_search_item(self, search_by_keyword, a_tag):
        if search_by_keyword.search_type == 'books':
            return ArticleSearchByKeywordItem(
                search_by_keyword=search_by_keyword,
                title=a_tag.text.strip(),
                url=self.base_url + a_tag['href']
            )

    def parse_book_detail(self, url):
        response = self.request_to_target_url(url=url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1', attrs={'class': 'Text Text__title1'}).text
        description = soup.find('div', attrs={'class': 'DetailsLayoutRightParagraph__widthConstrained'}).find_next(
            'span').text
        thumbnail = soup.find('img', attrs={'class': 'ResponsiveImage', 'role': 'presentation'})['src']
        author = self.parse_author(soup=soup)

        article = Article(
            author=author,
            title=title,
            description=description,
            html_source_code=response.text
        )

        category = self.parse_genre(soup=soup)

        return article, category

    def parse_author(self, soup):
        fullname = soup.find('span', attrs={'class': 'ContributorLink__name'}).text
        return Author(fullname=fullname)

    def parse_genre(self, soup):
        category = list()
        genre_soup = soup.find('ul', attrs={'class': 'CollapsableList', 'aria-label': 'Top genres for this book'})
        for genre in genre_soup.findAll('span', attrs={'class': 'Button__labelItem'}):
            if genre.text != '...more':
                category.append(Category(title=category.text))

        return category

