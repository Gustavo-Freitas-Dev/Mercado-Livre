import requests
from bs4 import BeautifulSoup
import os
import csv
import time

# Headers para a requisição
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}

# Entrada do usuário
input_produto = input('Digite o produto: ')
input_produto_formatado = input_produto.replace(' ', '-')

# URL inicial
url = f'https://lista.mercadolivre.com.br/{input_produto_formatado}'

# Nome do arquivo CSV
arquivo_csv = f'{input_produto}.csv'

# Criar cabeçalho no CSV se não existir
if not os.path.exists(arquivo_csv):
    with open(arquivo_csv, 'w', encoding='utf-8', newline='') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(['Título', 'Preço', 'Link'])

contador_pagina = 1

while True:
    # Fazer requisição
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"Erro ao acessar {url}. Código {r.status_code}")
        break

    site = BeautifulSoup(r.content, 'html.parser')

    # Encontra os cards dos produtos
    cards = site.find_all('li', class_='ui-search-layout__item')

    if not cards:
        print("Nenhum produto encontrado.")
        break

    for card in cards:
        # Buscar título
        titulo_elem = card.find('a', class_='poly-component__title')
        titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Sem título"

        # Buscar preço (procurando diretamente pelo valor)
        preco_elem = card.find('span', class_='andes-money-amount andes-money-amount--cents-superscript')
        if not preco_elem:
            preco_elem = card.find('span', 'andes-money-amount__fraction')
        preco = preco_elem.get_text(strip=True) if preco_elem else "Sem preço"

        # Buscar link
        link = titulo_elem['href'] if titulo_elem and titulo_elem.has_attr('href') else "Sem link"

        # Salvar no CSV
        with open(arquivo_csv, 'a', encoding='utf-8', newline='') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow([titulo, preco, link])

    print(f'Página {contador_pagina} feita!')

    # Buscar botão da próxima página
    proxima_pagina_elem = site.find('li', class_='andes-pagination__button--next')
    proxima_pagina_link = proxima_pagina_elem.find('a') if proxima_pagina_elem else None

    # Verifica se existe um link antes de tentar acessar 'href'
    url = proxima_pagina_link['href'] if proxima_pagina_link and proxima_pagina_link.has_attr('href') else None

    if url:
        print(f"Indo para a próxima página: {url}")
        contador_pagina += 1
        time.sleep(3)
    else:
        print("Não há mais páginas disponíveis.")
        break