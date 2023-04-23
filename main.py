import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
from time import sleep

headers = Headers(browser='firefox', os='win').generate()

vacancy_parsed = []
params = {
    'text': 'python django flask'
}
def list_vacancy_url():
    for count in range(0, 1):
        url = f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={count}&disableBrowserCache=true'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('div', class_='serp-item')
        for e in data:
            vacancy_url = e.find('a').get('href')
            yield vacancy_url

def vacancy_item():
    for vacancy_url in list_vacancy_url():
        response2 = requests.get(vacancy_url, params=params, headers=headers)
        sleep(3)
        soup2 = BeautifulSoup(response2.text, 'lxml')
        data = soup2.find('div', class_='bloko-columns-row')
        vacancy_info = data.find('div', class_='g-user-content').text
        if 'Django' or 'Flask' in vacancy_info:
            company_name = data.find('span', class_='vacancy-company-name').text
            salary = data.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite').text
            vacancy_data = data.find('div', class_='vacancy-company-redesigned')
            city = vacancy_data.find('p')
            vacancy_link = 'https://spb.hh.ru' + data.find('a', class_='bloko-button bloko-button_kind-success bloko-button_scale-large bloko-button_stretched')['href']
            vacancy_parsed.append(
                {
                    'название компании': company_name,
                    'зарплата': salary,
                    'город': city,
                    'ссылка': vacancy_link
                }
            )

if __name__ == '__main__':
    with open('vacancy_info.json', 'w', encoding='utf-8') as f:
        json.dump(vacancy_parsed, f)