from bs4 import BeautifulSoup
import requests 
import fake_useragent
import string
import time
import csv
import os.path

# <!---TO DO----!>
# 1. Обработка цены на товар, чтобы отсечь неинтересные объявления DONE
# 	- Добавление парсинга по страницам DONE
# 	- try-except
# 2. Выбор города для парсинга
# 3. Выбор по времени публикации
# 4. Вывод в файл(.csv or .txt) + проверка на существование в файле
# 5. Область поиска по станциям метро, если это Москва или Спб 



def get_page(url:str):
	'''Функция возвращает страницу по переданной в нее ссылке url'''
	user_agent = fake_useragent.UserAgent()
	user = user_agent.random
	headers = {
		'User-Agent': str(user)
	}
	response = requests.get(url, headers=headers)
	print(response)
	return response


def get_all_pages_links(response):
	'''Функция возвращает массив ссылок всех страниц товара, 1-ая страница которого передана в response'''
	pages = []
	soup = BeautifulSoup(response.content, 'html.parser')
	links = soup.findAll('a', class_='pagination-page')
	for link in links:
		href = 'https://www.avito.ru/' + link.get('href')
		pages.append(href)
	return pages


def get_all_content(response):
	'''Функция возвращает массив карточек товаров на странице'''
	soup = BeautifulSoup(response.content, 'html.parser')
	items = soup.findAll('div', class_='description item_table-description')
	return items


def get_data(item):
	'''Функция возвращает словарь, в котором содержится информация о товаре'''	
	data = {	'title': item.find('a', class_='snippet-link').get_text(strip=True),
				'city': item.find('span', class_='item-address__string').get_text(strip=True),
				'price': item.find('span', class_='snippet-price').get_text(strip=True),
				'link': 'https://www.avito.ru/' + item.find('a', class_='snippet-link').get('href')
			}
	return data


def file_write(dict):
	with open('parse_info.csv', 'a', newline='', encoding='utf8') as file:
			columns = ['title', 'city', 'price', 'link']
			writer = csv.DictWriter(file, fieldnames=columns)
			writer.writerow(dict)
		# else:
		# 	columns = ['title', 'city', 'price', 'link']
		# 	writer = csv.DictWriter(file, fieldnames=columns)
		# 	writer.writeheader()
		# 	writer.writerow(dict)
		# file.write(f'{dict["title"]} -> {dict["price"]} -> https://www.avito.ru/' + f'{dict["link"]}\n')


def main():
	url = 'https://www.avito.ru/rossiya/sobaki?q=той+пудель'
	dogs = []
	all_pages = get_all_pages_links(get_page(url))
	for page in all_pages:
		items = get_all_content(get_page(page))
		for item in items:
			item_data = get_data(item)
			if item_data not in dogs:
				# price = item_data.get('price').replace('₽', '')
				if item_data['title'].lower().find('вязк') == -1:
					print(item_data['city'])
					dogs.append(item_data)
					file_write(item_data)
		time.sleep(3)



	# for page in range(1, 6):
	# 	print(f'PAGE - {page}')
	# 	URL = f'https://www.avito.ru/rossiya/sobaki?q=той+пудель&p={page}'
	# 	print(URL)
	# 	response = requests.get(URL, headers=HEADERS)
	# 	soup = BeautifulSoup(response.content, 'html.parser')
	# 	items = soup.findAll('div', class_='description item_table-description')

		
	# 	for item in items:
	# 		dog_dict = {
	# 				'title': item.find('a', class_='snippet-link').get_text(strip=True),
	# 				'price': item.find('span', class_='snippet-price').get_text(strip=True),
	# 				'link': item.find('a', class_='snippet-link').get('href'),
	# 				'city': item.find('span', class_='item-address__string').get_text(strip=True)
	# 				}
	# 		if dog_dict not in dogs:
	# 			if dog_dict['city'] == 'Москва': 
	# 				if dog_dict['title'].lower().find('вязк') == -1:
	# 					dogs.append(dog_dict)
	# 					file_write(dog_dict)
	# 		# global dog
	# 		# for dog in dogs:
	# 		# 	dog_price = dog.get('price').replace('₽', '')
	# 		# 	if (dog_price != 'Цена не указана') and (dog_price != 'Бесплатно') and (int(dog_price.replace(' ', '')) >= 15000 and int(dog_price.replace(' ', '')) <= 50000): 
	# 		# 		# save()
	# 		# 		print(f'{dog["title"]} -> {dog["price"]} -> https://www.avito.ru/' + f'{dog["link"]}' )

	# 	time.sleep(3)
# city = input('В каком городе вы хотите найти пуделя? ')
if __name__ == '__main__':
	main() 