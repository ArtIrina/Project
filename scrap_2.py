from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import json

# 5 страницы c объявлениями на момент написания краулера.

def get_html(url):
    response = requests.get(url)
    return response.text

def get_all_links(html):
    soup = BeautifulSoup(html, features="html.parser")
    tds = soup.find(class_='photo-categories').find_all(class_='item')
    for td in tds:
        a = td.find(class_='image').find('a').get('href').split('/')[2]
        link = 'https://kinoagentstvo.ru/photos/' + a + '/'
        x = int(td.find(class_='text').text.split()[1])
        if (x > 1):
            get_all_links(get_html(link))
        if (x == 1):
            links.append(link)

def get_page_data(html):
    soup = BeautifulSoup(urlopen(html), features="html.parser")

    # заголовок
    try:
        header = str(soup.find('h1').text)
    except:
        header = ''

    # цена
    try:
        price = soup.find(class_='price').text
        price = int(''.join(i for i in price if i.isdigit()))
    except:
        price = 'По запросу'

    # описание (Сделать только кв.м и количество комнат???)
    try:
        description = str(soup.find(class_='photo_anketa').find(class_='comment').text)
    except:
        description = ''

    # фото
    try:
        pht = soup.find(class_='gallery photo_list_set').find_all(class_='img_s')
        photo = ''
        i = 0
        photo_count = len(pht)
        for p in pht:
            if (i == 10):
                break
            if (i == photo_count - 1 or i == 9):
                pht[i] = 'https://kinoagentstvo.ru' + p.attrs['href']
                photo += pht[i]
            else:
                pht[i] = 'https://kinoagentstvo.ru' + p.attrs['href'] + ' '
                photo += pht[i]
            i += 1
    except:
        photo = ''

    data = ({'link': html,                    # Ссылка на объект
             'description': description,      # Описание
             'photo': photo,                  # Фото
             'header': header,                # Заголовок
             'price': price})                 # Цена
    return data


def page_content(all_links, table):
    for object in (all_links):
        data = get_page_data(object)
        table.append(data)
        with open("data_2.json", "w") as write_file:
            json.dump(table, write_file, ensure_ascii=False)

table = []

def get_total_pages(html):
    soup = BeautifulSoup(html, features="html.parser")
    divs = soup.find('div', class_='bx-pagination-container')
    pages = divs.find_all('a')[-2].get('href')
    total_pages = pages.split('=')[1]
    return int(total_pages)


# ссылка первой страницы отличается по формату от остальных. Обработаем сначала отдельно первую, затем в цикле пройдем по остальным
# _1 = 'https://kinoagentstvo.ru/photos/'
# _2 = 'https://kinoagentstvo.ru/photos/?PAGEN_1=2'
# _3 = 'https://kinoagentstvo.ru/photos/?PAGEN_1=3'

links = []
url = 'https://kinoagentstvo.ru/photos/'
get_all_links(get_html(url))
page_content(links, table)
print("First page done")

count_pages = get_total_pages(get_html(url))

for i in range(2, count_pages + 1):
    links = []
    base = 'https://kinoagentstvo.ru/photos/?PAGEN_1='
    url = base + str(i)
    get_all_links(get_html(url))
    page_content(links, table)
    print(i)
