from bs4 import BeautifulSoup
import requests


def main():
    message = input()
    url = 'https://ek.ua/ek-list.php?search_=' + message
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    all_links = soup.find_all('a', class_='model-short-title')
    for item in all_links:
        url = 'https://ek.ua/ua' + item['href']
        # url = 'https://ek.ua/ua/AEROCOOL-EARL.htm'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        name = soup.select('.page-title')
        name = name[0].text

        price = soup.select('.desc-big-price')
        price = price[0].text

        img = soup.select('.img200 > img')
        img = img[0]['src']

        print(url, name, price, img, sep='\t')


main()
