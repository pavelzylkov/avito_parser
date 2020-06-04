from bs4 import BeautifulSoup
import requests 
import fake_useragent
import string
import time
import csv

# <!---TO DO----!>

# 2. Выбор города для парсинга
# 3. Выбор по времени публикации - не знаю зачем??
# 5. Область поиска по станциям метро, если это Москва или Спб 



def get_page(url:str):
	'''Возвращает страницу по переданной в нее ссылке url'''
	user_agent = fake_useragent.UserAgent()
	user = user_agent.random
	headers = {
		'User-Agent': str(user)
	}
	response = requests.get(url, headers=headers)
	return response


def get_all_pages_links(response):
	'''Возвращает массив ссылок всех страниц товара, 1-ая страница которого передана в response'''
	pages = []
	soup = BeautifulSoup(response.content, 'html.parser')
	links = soup.findAll('a', class_='pagination-page')
	for link in links:
		href = 'https://www.avito.ru/' + link.get('href')
		pages.append(href)
	return pages


def get_all_content(response):
	'''Возвращает массив карточек товаров на странице'''
	soup = BeautifulSoup(response.content, 'html.parser')
	try:
		items = soup.findAll('div', class_='description item_table-description')
	except Exception:
		print('ERROR!!! PAGE NOT FOUND')
	return items


def get_data(item):
	'''Возвращает словарь, в котором содержится информация о товаре'''
	try:
		title = item.find('a', class_='snippet-link').get_text(strip=True)
	except Exception:
		title = ''
	try:
		city = item.find('span', class_='item-address__string').get_text(strip=True)
	except Exception:
		city = ''
	try:
		price = item.find('span', class_='snippet-price').get_text(strip=True)
	except Exception:
		price = ''	
	try:
		link = 'https://www.avito.ru/' + item.find('a', class_='snippet-link').get('href')
	except Exception:
		link = ''

	data = {	'title': title,
				'city': city,
				'price': price,
				'link': link }
	return data


def create_file():
	'''Cоздает пустой файл для записи'''
	with open('parse_info.csv', 'w', newline='', encoding='utf8') as file:
			columns = ['title', 'city', 'price', 'link']
			writer = csv.DictWriter(file, fieldnames=columns)
			writer.writeheader()


def file_write(dict):
	'''Записывает данные товару в файл из словаря dict'''
	with open('parse_info.csv', 'a', newline='', encoding='utf8') as file:
			columns = ['title', 'city', 'price', 'link']
			writer = csv.DictWriter(file, fieldnames=columns)
			writer.writerow(dict)


def main():
	url = 'https://www.avito.ru/rossiya/sobaki?q=той+пудель'
	dogs = []
	create_file()
	all_pages = get_all_pages_links(get_page(url))
	for page in all_pages:
		items = get_all_content(get_page(page))
		for item in items:
			item_data = get_data(item)
			if item_data not in dogs:
				if item_data['title'].lower().find('вязк') == -1:
					dogs.append(item_data)
					file_write(item_data)
		time.sleep(3)


if __name__ == '__main__':
	main() 