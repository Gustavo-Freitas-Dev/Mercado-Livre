import requests
from bs4 import BeautifulSoup as bs4




def buscar(item:str) -> list[dict]:
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


def _paginar(html:str) -> str:
    '''Verifica a existencia de uma proxima pagina e retorna o link dela'''
    

    html:bs4 = bs4(html, 'html.parser')
    next_url = html.select('li.andes-pagination__button.andes-pagination__button--next > a')[0].get('href', '')
    return next_url


def _raspagem(html:str) -> list[dict]:
    '''Faz a raspagem dos dados no HTML'''
    

    html:bs4 = bs4(html, 'html.parser')
    CARDS_HTML = html.select('li div.andes-card')

    CARDS:list[dict] = []
    CARD_SELECTOR = {
        'name': 'div.poly-card__content h3 > a',
        'old_value': 'div.poly-component__price s span.andes-money-amount__fraction',
        'value': 'div.poly-component__price div.poly-price__current span.andes-money-amount__fraction',
        'discount': 'div.poly-component__price span.andes-money-amount__discount'
    }

    # captura dos valores
    for card in CARDS_HTML:
        CARD = {}
        for selector in set(CARD_SELECTOR.keys()): 
            result = card.select(CARD_SELECTOR[selector])
            CARD[selector] = result

        CARDS.append(CARD)

    # tratamento dos valores
    for card in CARDS:
        for key in set(card.keys()):
            card[key] = card[key][0].text if card[key] != [] else ''
            card[key] = float(card[key].replace('.','').replace(',','.')) if key in ['old_value', 'value'] and card[key] != '' else card[key]
            card[key] = int(card[key][:card[key].find('%')]) if key == 'discount' and '%' in card[key] else card[key]
            card[key] = 0 if card[key] == '' and key in ['old_value', 'value', 'discount'] else card[key]

    return CARDS


def csv():
    '''Converte o resultado para CSV'''
    ...