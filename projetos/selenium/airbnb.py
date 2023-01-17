import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

dados_hospedagens = []

options = Options()
# options.add_argument('--headless')
options.add_argument('window-size=400,800')

navegador = webdriver.Chrome(options=options)

navegador.get('https://www.airbnb.com')

sleep(2)

input_place = navegador.find_element_by_tag_name('input')
input_place.send_keys('São Paulo')
input_place.submit()

sleep(0.5)

button_stay = navegador.find_element_by_css_selector('button > img')
button_stay.click()

sleep(0.5)

nextButton = navegador.find_elements_by_tag_name('button')[-1]
nextButton.click()

sleep(0.5)

# Definindo dois adultos
adultButton = navegador.find_elements_by_css_selector('button > span > svg > path[d="m2 16h28m-14-14v28"]')[0]
adultButton.click()
sleep(1)
adultButton.click()
sleep(1)


searchButton = navegador.find_elements_by_tag_name('button')[-1]
searchButton.click()

sleep(4)

page_content = navegador.page_source

hospedagens = BeautifulSoup(page_content, 'html.parser')

for hospedagem in hospedagens:
    #print(hospedagem.prettify())

    hospedagem_descricao = hospedagem.find('meta', attrs={'itemprop': 'name'})
    hospedagem_url = hospedagem.find('meta', attrs={'itemprop': 'url'})

    hospedagem_descricao = hospedagem_descricao['content']

    hospedagem_url = hospedagem_url['content']

    print('Descricao: ', hospedagem_descricao)
    print('Url: ', hospedagem_url)

    hospedagem_detalhes = hospedagem.find('div', attrs={'style': 'margin_buttom: 2px;'}).find_all('li')

    #hospedagem_detalhes = hospedagem_detalhes[0].text + hospedagem_detalhes[1].text
    hospedagem_detalhes = ''.join([detalhe.text for detalhe in hospedagem_detalhes])

    print('Detalhes da hospedagem: ', hospedagem_detalhes)

    preco = hospedagem.findAll('span')[-1].text

    print('Preço da hospedagem: ', preco)

    print()

    dados_hospedagens.append([hospedagem_descricao, hospedagem_url, hospedagem_detalhes, preco])

dados = print(pd.DataFrame(dados_hospedagens, columns=['Descrição', 'Url', 'Detalhes', 'Preço']))

dados.to_csv('hospedagens.csv', index=False)