from datetime import datetime
from constatns import SEARCH_PAGE_COUNT


class Author:
    def __init__(self, fullname):
        self.fullname = fullname

    def __str__(self):
        return self.fullname


class Category:
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return self.title


class Article:
    def __init__(self, author, title, description, html_source_code):
        self.author = author
        self.title = title
        self.description = description
        self.html_source_code = html_source_code

    def __str__(self):
        return self.title


class ArticleCategory:
    def __init__(self, article, category):
        self.article = article
        self.category = category

    def __str__(self):
        return f'{self.article.title}({self.category.title})'


class Keyword:
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return self.title


class SearchByKeyword:
    def __init__(self, keyword, page_count=SEARCH_PAGE_COUNT):
        self.keyword = keyword
        self.page_count = page_count
        self.created_at = datetime.now()

    def __str__(self):
        return self.keyword.title


class ArticleSearchByKeywordItem:
    def __init__(self, search_by_keyword, title, url):
        self.search_by_keyword = search_by_keyword
        self.title = title
        self.url = url
        self.book = None

    def __str__(self):
        return f'{self.title}({self.search_by_keyword.keyword.title})'
