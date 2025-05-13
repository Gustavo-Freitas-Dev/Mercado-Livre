import requests
from bs4 import BeautifulSoup
import re
from time import sleep


def requisicao(session: requests.Session, url: str) -> BeautifulSoup:
    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException:
        print(f"Erro ao acessar: {url}")
        return None


def extrair_preco_numerico(preco_str):
    preco_limpo = preco_str.replace(".", "").replace(",", "")
    preco_digitos = re.sub(r'[^\d]', '', preco_limpo)
    return int(preco_digitos) if preco_digitos else float('inf')

def buscar_produtos(produto: str):
    dados = []
    session = requests.Session()
    url = f"https://lista.mercadolivre.com.br/{produto.replace(' ', '-')}"
    
    print(f"🔍 Raspando página 1 - {url}")
    soup = requisicao(session, url)
    if not soup:
        print("❌ Erro ao carregar a página.")
        return []

    cards = soup.find_all('li', class_='ui-search-layout__item')
    for card in cards:
        link_tag = card.find('a', class_='poly-component__title')
        titulo_elem = card.find('h3', class_='poly-component__title-wrapper')
        preco_elem = card.find('span', class_='andes-money-amount__fraction')
        preco_centavos = card.find('span', class_='andes-money-amount__cents')

        titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Sem título"

        if preco_elem:
            preco = f"R$ {preco_elem.get_text(strip=True)}"
            if preco_centavos:
                preco += f",{preco_centavos.get_text(strip=True)}"
            else:
                preco += ",00"

            preco_numerico = extrair_preco_numerico(preco)
            link = link_tag['href'] if link_tag and link_tag.has_attr('href') else "Sem link"

            dados.append({
                "Título": titulo,
                "Preço": preco,
                "Link": link,
                "preco_numerico": preco_numerico
            })


    sleep(1)
    return sorted(dados, key=lambda x: x.get("preco_numerico", float('inf')))


if __name__ == "__main__":
    termo = "PS5"
    produtos = buscar_produtos(termo)

    for p in produtos:
        print(p['Título'])
        print(p['Preço'])
        print(p['Link'])
        print('---'*30)
