import requests
# from bs4 import BeautifulSoup




def buscar(item:str) -> list[object]:
    '''Busca no site do mercado live o item desejado'''
    
    
    item = item.replace(' ','-') if ' ' in item else item
    url = f'https://lista.mercadolivre.com.br/{item}'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
    
    RESP = []
    while True:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            html = response.text
            RESP += _raspagem(html)
            url = _paginar(html)
        
        if url == '':
            break

    return RESP


def _paginar(html) -> str:
    '''Verifica a existencia de uma proxima pagina e retorna o link dela'''
    ...


def _raspagem(html:str) -> list[object]:
    '''Faz a raspagem dos dados no HTML'''
    ...

def csv():
    '''Converte o resultado para CSV'''
    ...