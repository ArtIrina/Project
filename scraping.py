from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import json

# 171 страница c объявлениями на момент написания краулера.

def get_html(url):
    response = requests.get(url)
    return response.text

def get_all_links(html):
    soup = BeautifulSoup(html, features="html.parser")
    tds = soup.find_all(class_='living-search-item offers-search__item')
    links = []
    for td in tds:
        a = td.find('a', class_='link').get('href')
        link = 'https://moskva.n1.ru' + a
        links.append(link)
    return links

def get_page_data(html):
    soup = BeautifulSoup(urlopen(html), features="html.parser")

    # заголовок (Адрес: ул., дом???)
    try:
        header = str(soup.find(class_='title').text)
    except:
        header = ''

    # цена
    try:
        price = soup.find(class_='price').text
        price = int(''.join(i for i in price if i.isdigit()))
    except:
        price = ''

    # описание (Сделать только кв.м и количество комнат???)
    try:
        description = str(soup.find(class_='foldable-description card-living-content__description').find(class_='text').text)
        #print(description)
    except:
        description = ''

    # фото
    try:
        pht = soup.find_all(class_='image')
        photo = ''
        i = 0
        photo_count = len(pht)
        for p in pht:
            if (i == 10):
                break
            if (i == photo_count - 1 or i == 9):
                pht[i] = p.attrs['src']
                photo += pht[i]
            else:
                pht[i] = p.attrs['src'] + ' '
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
    for link in (all_links):
        data = get_page_data(link)
        table.append(data)

    with open("data_file.json", "w") as write_file:
        json.dump(table, write_file, ensure_ascii=False)


table = []

# ссылка первой страницы отличается по формату от остальных. Обработаем сначала отдельно первую, затем в цикле пройдем по остальным
# _1 = 'https://moskva.n1.ru/search/?rubric=flats&deal_type=sell&price_max=35000000&rooms=2%2C3'
# _2 = 'https://moskva.n1.ru/search/?price_max=35000000&rooms=2%2C3&deal_type=sell&rubric=flats&page=2'
# _3 = 'https://moskva.n1.ru/search/?price_max=35000000&rooms=2%2C3&deal_type=sell&rubric=flats&page=3'

url = 'https://moskva.n1.ru/search/?rubric=flats&deal_type=sell&price_max=35000000&rooms=2%2C3'
all_links = get_all_links(get_html(url))
page_content(all_links, table)
print("First page done")

for i in range(2, 41): # После 40 сраницы идет много пустых, необустроенных квартир, такие варианты считаю не подходящими для площадок для киносъемок (на момент написания краулера)
    base = 'https://moskva.n1.ru/search/?price_max=35000000&rooms=2%2C3&deal_type=sell&rubric=flats&page='
    url = base + str(i)
    all_links = get_all_links(get_html(url))
    page_content(all_links, table)
    print(i)