#importa as bibliotecas
import time as delay
from urllib.request import urlopen

#definição para testar a conexão com a internet
def conexao():
    try:
        urlopen('https://www.materdei.edu.br/pt', timeout=1)
        return True
    except:
        return False
    
#verifica se existe conexão ou não
if conexao() == True:
    print('Tem conexão')
else:
    print('PUTs')
