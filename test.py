import tkinter as tk
import requests
from bs4 import BeautifulSoup
from PIL import ImageTk, Image

DEFAULT_NUMBER_OF_PAGES = 5
DEFAULT_KEYWORD_INPUT = 'games'
BASE_URL = 'https://search.techcrunch.com/search;_ylt=AwrFOlrOTAtmG90DT2ynBWVH;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-?p={keyword}&pz=10&bct=0&b={output}&pz=10&bct=0&xargs=0'

class SearchByUserInput:
    def __init__(self, pages, url, keyword, total_search):
        self.pages = pages
        self.url = url
        self.keyword = keyword
        self.total_search = total_search

    def search_engine(self):
        for i in range(1, int(self.total_search * 10) + 1):
            response = requests.get(self.url.format(
                keyword=self.keyword, output=i))
            soup = BeautifulSoup(response.text, features="html.parser")
            result = soup.findAll('h4', {'class': 'pb-10'})
            date = soup.findAll('span', style='color:#777')
            author = soup.findAll('span', style='color:#333; font-weight: 700')
            body = soup.findAll('p', style="color: #777")
            link = soup.findAll('a', {'class': 'fz-20 lh-22 fw-b'})
            total_result_in_website = [span.text for div in soup.findAll(
                'div', {'class': 'compPagination'}) for span in div.findAll('span')]

            for re, de, auth, bo, l, t in zip(result, date, author, body, link, total_result_in_website):
                print('title=', re.text),
                print('date_posted=', de.text),
                print('authors=', auth.text),
                print('summary=', bo.text),
                print('link=', l['href']),
                print('keywords=', self.keyword),
                print('websit_total_results=', t),
                print('total pages number:', self.pages)
                print('total number of the result:', self.total_search)
                total_results = ''.join(filter(str.isdigit, t))
                print('*' * 80)
                if self.total_search > int(total_results):
                    print('Your request should be less then the total website results:\n'
                          'total results in website:', total_results, '\nTry again')
                    break

def search():
    keyword = keyword_entry.get()
    pages = pages_entry.get()
    try:
        search_by_user_input_instance = SearchByUserInput(
            int(pages), BASE_URL, keyword, int(pages) * 10)
        results = search_by_user_input_instance.search_engine()
        for i, result in enumerate(results):
            title = result[0]
            date_posted = result[1]
            authors = result[2]
            summary = result[3]
            link = result[4]
            keywords = result[5]
            website_total_results = result[6]
            total_pages_number = result[7]
            total_number_of_result = result[8]
            image_link = result[9]
            label = tk.Label(result_frame, text=title)
            label.grid(column=0, row=i)
            label = tk.Label(result_frame, text=date_posted)
            label.grid(column=1, row=i)
            label = tk.Label(result_frame, text=authors)
            label.grid(column=2, row=i)
            label = tk.Label(result_frame, text=summary)
            label.grid(column=3, row=i)
            label = tk.Label(result_frame, text=link)
            label.grid(column=4, row=i)
            label = tk.Label(result_frame, text=keywords)
            label.grid(column=5, row=i)
            label = tk.Label(result_frame, text=website_total_results)
            label.grid(column=6, row=i)
            label = tk.Label(result_frame, text=total_pages_number)
            label.grid(column=7, row=i)
            label = tk.Label(result_frame, text=total_number_of_result)
            label.grid(column=8, row=i)
            img = ImageTk.PhotoImage(Image.open(requests.get(image_link, stream=True).raw))
            label = tk.Label(result_frame, image=img)
            label.grid(column=9, row=i)
    except Exception as e:
        print(e)

def close_window():
    window.destroy()

window = tk.Tk()
window.title("TechCrunch Search")
window.geometry("1200x600")

keyword_label = tk.Label(window, text="Keyword:")
keyword_label.grid(column=0, row=0)

keyword_entry = tk.Entry(window)
keyword_entry.grid(column=1, row=0)

pages_label = tk.Label(window, text="Pages:")
pages_label.grid(column=0, row=1)

pages_entry = tk.Entry(window)
pages_entry.grid(column=1, row=1)

search_button = tk.Button(window, text="Search", command=search)
search_button.grid(column=0, row=2)

exit_button = tk.Button(window, text="Exit", command=close_window)
exit_button.grid(column=1, row=2)

result_frame = tk.Frame(window)
result_frame.grid(column=0, row=3, columnspan=2)

window.mainloop()