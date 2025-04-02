from utils.Mercado_livre import buscar

if '__main__' == __name__:
    PRODUTOS = buscar('ps5')
    for produto in PRODUTOS:
        print(produto)