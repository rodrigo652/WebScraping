import requests
from bs4 import BeautifulSoup
import pandas as pd

lista_noticias = []

response = requests.get('https://g1.globo.com/')

content = response.content

site = BeautifulSoup(content, 'html.parser')

noticias = site.findAll('div', attrs={'class': 'feed-post-body'}) #html da noticia

for noticia in noticias:
    titulo = noticia.find('a', attrs={'class': 'feed-post-link'}) #titulo da noticia
    print(titulo.text)
    print(titulo['href']) #link da noticia

    subtitulo = noticia.find('div', attrs={'class': 'feed-post-body-resumo'})#subtitulo da noticia
    if(subtitulo):
        print(subtitulo.text)
        lista_noticias.append([titulo.text, subtitulo.text, titulo['href']])
    else:
        lista_noticias.append([titulo.text, '', titulo['href']])

news = pd.DataFrame(lista_noticias, columns=['Título', 'Subtítulo', 'Link'])

#news.to_excel('noticias.xlsx', index=False)

print(news)