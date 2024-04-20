from basic_methods import BASE_CATEGORY_URL, BASE_URL
from category_scraper import user_keyword_input, user_page_number_input, user_pages_input, SearchByCategory, \
    SearchByUserInput

task = int(
    input('Enter a number:\n1.search by category\n2.search by your input---> '))
if task == 1:
    search_by_category_instance = SearchByCategory(
        BASE_CATEGORY_URL, user_pages_input())
    search_by_category_instance.search_loop()
elif task == 2:
    search_by_user_input_instance = SearchByUserInput(
        user_pages_input(), BASE_URL, user_keyword_input(), user_page_number_input())
    search_by_user_input_instance.search_engine()
    # search_by_user_input_instance.search_engine()
