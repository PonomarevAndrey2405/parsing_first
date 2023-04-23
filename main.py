import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
from time import sleep

headers = Headers(browser='firefox', os='win').generate()
#С помощью этой функции получаем url вакансий (всех)
def list_vacancy_url():
    for count in range(0, 41):
        url = f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={count}&disableBrowserCache=true'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('div', class_='serp-item')
        for e in data:
            vacancy_url = e.find('a').get('href')
            yield vacancy_url
#С помощью этой функции заходим в описание каждой вакансии, при помощи функции list_vacancy_url,
#и достаём от туда название компании, зарплату и город
def vacancy_item():
    for vacancy_url in list_vacancy_url():
        response2 = requests.get(vacancy_url, headers=headers)
        sleep(3)
        soup2 = BeautifulSoup(response2.text, 'lxml')
        data = soup2.find('div', class_='bloko-columns-row')
        vacancy_info = data.find('div', class_='g-user-content').text
        if 'Django' or 'Flask' in vacancy_info:
            company_name = data.find('span', class_='vacancy-company-name').text
            salary = data.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite')
            if salary == None:
                yield None
            else:
                yield salary.text
            vacancy_data = data.find('div', class_='vacancy-company-redesigned')
            city = vacancy_data.find('p').text
            yield company_name, salary, city

#Запись в файл тех вакансий, которые в описании имеют "Django" или "Flask"
dictionary = {
    company_name: vacancy_item(company_name),   #запись названия компании
    salary: vacancy_item(salary),         #запись зарплаты
    city: vacancy_item(city),           #запись города
    vacancy_url: list_vacancy_url(vacancy_url) #запись url вакансии
}
with open('vacancy_info.json', 'w') as f:
    json.dump(dictionary, f)