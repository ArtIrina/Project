from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import json

# 4 страницы c объявлениями на момент написания краулера.

def get_html(url):
    response = requests.get(url)
    return response.text


def get_all_links(url, html):
    soup = BeautifulSoup(html, features="html.parser")
    tds = soup.find(class_='albums').find_all(class_='item')
    for td in tds:
        a = td.find(class_='image').find('a').get('href').split('/')[2]
        link = 'https://kinoagentstvo.ru/photos/' + a + '/'
        x = int(td.find(class_='info').find('b').text)
        if (int(td.find(class_='info').find('b').text) > 1):
            get_all_links(link, get_html(link))
        if (x == 1):
            # print(a)
            links.append(link)


def get_page_data(html):
    soup = BeautifulSoup(urlopen(html), features="html.parser")

    # заголовок
    try:
        header = str(soup.find(class_='content').find('h1').text)
        #print(header)
    except:
        header = ''
        #print(header)

    # цена
    try:
        price = soup.find(class_='price').text
        price = int(''.join(i for i in price if i.isdigit()))
        #print(price)
    except:
        price = 'По запросу'
        #print(price)

    # описание (Сделать только кв.м и количество комнат)
    try:
        description = str(soup.find(class_='photo_anketa').find(class_='comment').text)
        #print(description)
    except:
        description = ''
        #print(description)

    # фото
    try:
        photo = soup.find(class_='gallery photo_list_set').find_all(class_='img_s')
        i = 0
        for p in photo:
            # t = p.attrs
            # v = t['src']
            photo[i] = 'https://kinoagentstvo.ru' + p.attrs['href']
            i += 1
    except:
        photo = ''

    data = ({'link': html,  # Ссылка на объект
             'description': description,      # Описание
             'photo': photo,                  # Фото
             'header': header,                # Заголовок
             'price': price})  # Цена
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
    divs = soup.find('div', class_='photo_object_list photo_list_set')
    pages = divs.find_all(class_='text')[-1].find_all('a')[-1].get('href')
    total_pages = pages.split('=')[1]
    return int(total_pages)


# ссылка первой страницы отличается по формату от остальных. Обработаем сначала отдельно первую, затем в цикле пройдем по остальным
# _1 = 'https://kinoagentstvo.ru/photos/'
# _2 = 'https://kinoagentstvo.ru/photos/?PAGEN_1=2'
# _3 = 'https://kinoagentstvo.ru/photos/?PAGEN_1=3'

links = []
url = 'https://kinoagentstvo.ru/photos/'
get_all_links(url, get_html(url))
# print(len(links))
# print(links)
page_content(links, table)
# a = ['https://kinoagentstvo.ru/photos/7728/']
# page_content(a, table)

count_pages = get_total_pages(get_html(url))
# print(count_pages)

for i in range(2, count_pages + 1):
    links = []
    base = 'https://kinoagentstvo.ru/photos/?PAGEN_1='
    url = base + str(i)
    get_all_links(get_html(url))
    page_content(links, table)
#     print(i)

# print(len(table))
